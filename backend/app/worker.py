import json
import os
from datetime import datetime
from hashlib import sha256
from pathlib import Path
import traceback

from app.models import TVLSettings
import celery
import numpy as np
import pandas as pd
import sentry_sdk

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.tvl import (
    populate,
    tvl,
)

if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN))


class TaskFailure(Exception):
    pass


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def dummy_task():
    print("runnig dummy task")
    folder = "/tmp/celery"
    os.makedirs(folder, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%s")
    with open(f"{folder}/task-{now}.txt", "w") as f:
        f.write("hello!")


# @celery_app.task(name="simulate_tvl")
@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    name="app.worker.simulate_tvl",
)
def simulate_tvl(_self, sim_settings: dict) -> None:
    try:

        settings = TVLSettings.model_validate_json(sim_settings)
        success = True
        sorted_population, _population_index = populate(
            size=settings.size,
            lower_bound=settings.lower_bound,
            upper_bound=settings.upper_bound,
            mean=settings.mean,
            std=settings.std,
        )

        tvl_value = tvl(
            talent=sorted_population,
            time=settings.iterations,
            unlucky_event=settings.unlucky_event,
            lucky_event=settings.lucky_event,
        )

        most_successful_index = np.argmax(tvl_value)

        file_name = sha256(json.dumps(settings.model_dump_json()).encode()).hexdigest()

        print(
            f"Highest position is:{tvl_value[most_successful_index]} with talent:{sorted_population[most_successful_index]}"
        )
        print(
            f"Average talent of successful individuals is:{sorted_population[tvl_value > 0].mean()}"
        )

        pathstr = f"/storage/tvl/{settings.id_user}/{file_name}.parquet"
        path = Path(pathstr).mkdir(parents=True, exist_ok=True)
        pd.DataFrame(
            zip(sorted_population, tvl_value), columns=["talent", "position"]
        ).to_parquet(path)

    except Exception as e:
        success = False
        traceback_str = traceback.format_exc().split("\n")
        print("\n" + f"Error: {str(e)}\nTraceback: {traceback_str}" + "\n")
        _self.update_state(
            state=celery.states.FAILURE,
            meta={
                "exc_type": type(e).__name__,
                "exc_message": traceback.format_exc().split("\n"),
                "custom": "...",
            },
        )
        raise Exception(traceback_str)

    finally:
        return file_name if success else f"TASK FAILED: \n{traceback_str}"


def retrieve_task_status() -> None:
    try:
        celery_app.current_task.update_state(
            state="PROGRESS", meta={"status": "retrieving task status"}
        )
        i = celery_app.control.inspect()
        status = {
            "registered": i.registered(),
            "active": i.active(),
            "reserved": i.reserved(),
            "revoked": i.revoked(),
            "stats": i.stats(),
        }
        pass
    except Exception as e:
        print(str(e))
    finally:
        return status
