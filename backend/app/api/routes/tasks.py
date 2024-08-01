import os
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.deps import CurrentUser, SessionDep
from app.models import TVLSettings
from app.worker import list_tasks, simulate_tvl, retrieve_task_status


class TaskOut(BaseModel):
    id: str
    status: str


router = APIRouter()


@router.get("/")
def read_Tasks(
    session: SessionDep,  # noqa: ARG001
    current_user: CurrentUser,  # noqa: ARG001
    skip: int = 0,  # noqa: ARG001
    limit: int = 100,  # noqa: ARG001
) -> Any:
    """
    Retrieve Tasks.
    """

    return "Tasks"


@router.post("/generate-tvl")
def tvl(
    session: SessionDep,  # noqa: ARG001
    current_user: CurrentUser,  # noqa: ARG001
    settings: TVLSettings,
) -> Any:
    """
    Generate a TVL simulation.
    """
    settings.id_user = current_user.id
    task = simulate_tvl.delay(settings.model_dump_json())
    return task.id


@router.get("/list-tasks")
def get_task_status(
    session: SessionDep,  # noqa: ARG001
    current_user: CurrentUser,  # noqa: ARG001
) -> Any:
    """
    List available tasks.
    """

    return list_tasks()


@router.get("/clear-storage")
def clear(
    session: SessionDep,  # noqa: ARG001
    current_user: CurrentUser,  # noqa: ARG001
    skip: int = 0,  # noqa: ARG001
    limit: int = 100,  # noqa: ARG001
) -> Any:
    """
    Clear local storage of task results.
    """
    os.removedirs("/tmp/")
    return "Removed sorted_population.csv"
