import json
import os
from datetime import datetime
from hashlib import sha256

import numpy as np
import sentry_sdk

from app.core.celery_app import celery_app
from app.core.config import settings
from app.core.tvl import (
    populate,
    tvl,
)

if settings.SENTRY_DSN:
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN))


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
    sorted_population, _population_index = populate(
        size=sim_settings["size"],
        lower_bound=sim_settings["lower_bound"],
        upper_bound=sim_settings["upper_bound"],
        mean=sim_settings["mean"],
        std=sim_settings["std"],
    )

    tvl_value = tvl(
        talent=sorted_population, time=80, unlucky_event=0.3, lucky_event=0.3
    )

    most_successful_index = np.argmax(tvl_value)

    file_name = sha256(json.dumps(sim_settings).encode()).hexdigest()

    print(f"file_name: {file_name} (not saving to disk)")

    # tvl_value.tofile("/tmp/tvl_value.csv",sep=",")
    # np.savetxt(f"/tmp/tvl/{file_name}.csv", sorted_population, delimiter=",")

    print(f"Population is:{sorted_population.tolist()}")
    print(
        f"Highest position is:{tvl_value[most_successful_index]} with talent:{sorted_population[most_successful_index]}"
    )

    return True
