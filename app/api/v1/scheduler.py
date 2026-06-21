from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_scheduler_service, require_admin
from app.schemas.scheduler import SchedulerRunResponse, SchedulerStatus
from app.services.scheduler_service import SchedulerService

router = APIRouter(prefix="/scheduler", tags=["Scheduler"])


@router.post("/run", response_model=SchedulerRunResponse, dependencies=[Depends(require_admin)])
def run_scheduler(
    scheduler_service: Annotated[SchedulerService, Depends(get_scheduler_service)],
) -> SchedulerRunResponse:
    return scheduler_service.trigger_run()


@router.get("/status", response_model=SchedulerStatus, dependencies=[Depends(require_admin)])
def get_scheduler_status(
    scheduler_service: Annotated[SchedulerService, Depends(get_scheduler_service)],
) -> SchedulerStatus:
    return scheduler_service.get_status()
