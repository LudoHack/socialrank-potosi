from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import tempfile, os
from database import get_db
from services.excel_parser import parse_excel, generate_template

router = APIRouter()

@router.post("/{project_id}")
async def upload_excel(
    project_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .xlsx o .xls")

    contents = await file.read()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        result = parse_excel(tmp_path, project_id, db)
    finally:
        os.unlink(tmp_path)

    return {"ok": True, "importados": result}

@router.get("/template")
def download_template():
    path = generate_template()
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="template_etnografica.xlsx"
    )
