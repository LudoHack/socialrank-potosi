from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from database import get_db
from models.risk import Risk

router = APIRouter()

class RiskSchema(BaseModel):
    project_id: int
    tema: str
    descripcion: Optional[str] = None
    nivel: Optional[str] = "amarillo"
    velocidad_crecimiento: Optional[int] = 3
    narrativas_relacionadas: Optional[List[int]] = []
    fecha_deteccion: Optional[date] = None
    activo: Optional[bool] = True

@router.get("/{project_id}")
def list_risks(project_id: int, db: Session = Depends(get_db)):
    ORDEN = {"rojo": 0, "amarillo": 1, "verde": 2}
    items = db.query(Risk).filter(Risk.project_id == project_id, Risk.activo == True).all()
    items.sort(key=lambda r: (ORDEN.get(r.nivel, 3), -(r.velocidad_crecimiento or 0)))
    return [{"id": r.id, "tema": r.tema, "descripcion": r.descripcion, "nivel": r.nivel,
             "velocidad_crecimiento": r.velocidad_crecimiento,
             "narrativas_relacionadas": r.narrativas_relacionadas or [],
             "fecha_deteccion": str(r.fecha_deteccion) if r.fecha_deteccion else None,
             "activo": r.activo} for r in items]

@router.post("/")
def create_risk(data: RiskSchema, db: Session = Depends(get_db)):
    item = Risk(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return {"id": item.id}

@router.put("/{item_id}")
def update_risk(item_id: int, data: RiskSchema, db: Session = Depends(get_db)):
    item = db.query(Risk).filter(Risk.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit(); return {"ok": True}

@router.delete("/{item_id}")
def delete_risk(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Risk).filter(Risk.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    db.delete(item); db.commit(); return {"ok": True}
