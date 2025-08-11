from typing import Dict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.src.containers.container import Container
from app.src.schemas.report_schema import ReportResponse
from app.src.services import ReportService

router = APIRouter(prefix="/report")


@router.get("", response_model=ReportResponse)
@inject
async def generate_report(
    report_service: ReportService = Depends(Provide[Container.report_service]),
) -> Dict[str, str]:
    # await report_service.start_report_in_process()
    await report_service.start_report_in_thread()
    return {"detail": "Report is generated"}
