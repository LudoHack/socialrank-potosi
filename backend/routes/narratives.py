from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db
from models.narrative import Narrative

router = APIRouter()

class NarrativeSchema(BaseModel):
    project_id: int
    texto: str
    tipo: Optional[str] = "dominante"
    actor_politico: Optional[str] = None
    fecha_deteccion: Optional[date] = None
    peso: Optional[float] = 5.0

@router.get("/{project_id}")
def list_narratives(project_id: int, db: Session = Depends(get_db)):
    items = db.query(Narrative).filter(Narrative.project_id == project_id).order_by(Narrative.peso.desc()).all()
    return [{"id": n.id, "texto": n.texto, "tipo": n.tipo, "actor_politico": n.actor_politico,
             "fecha_deteccion": str(n.fecha_deteccion) if n.fecha_deteccion else None,
             "peso": n.peso, "created_at": str(n.created_at)} for n in items]

@router.post("/")
def create_narrative(data: NarrativeSchema, db: Session = Depends(get_db)):
    item = Narrative(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return {"id": item.id}

@router.put("/{item_id}")
def update_narrative(item_id: int, data: NarrativeSchema, db: Session = Depends(get_db)):
    item = db.query(Narrative).filter(Narrative.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit(); return {"ok": True}

@router.delete("/{item_id}")
def delete_narrative(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Narrative).filter(Narrative.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    db.delete(item); db.commit(); return {"ok": True}
