from fastapi import APIRouter
from fastapi.responses import FileResponse

from services.report_generator import generate_report

router = APIRouter()

@router.get("/report")
def report():
    pdf_path = generate_report()

    return FileResponse(
        path=pdf_path,
        media_type='application/pdf', #type du fichier = pdf
        filename='audit_report.pdf'  #nom du fichier
    )

@router.get("/report/{scan_id}")
def report(scan_id: int):
    # génère un PDF filtré sur ce scan ;
    path = generate_report(output_path=f"report_{scan_id}.pdf", scan_id=scan_id)
    return FileResponse(path, media_type="application/pdf", filename=f"audit-report_{scan_id}.pdf")