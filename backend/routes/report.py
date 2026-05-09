from fastapi import APIRouter
from fastapi.responses import FileResponse

from services.report_generator import generate_report

router = APIRouter()

@router.get("/report")
def report():
    pdf_path = generate_report()

    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename='audit_report.pdf'
    )