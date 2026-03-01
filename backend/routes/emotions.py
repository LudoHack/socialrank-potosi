from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db
from models.emotion import Emotion

router = APIRouter()

class EmotionSchema(BaseModel):
    project_id: int
    tipo: str
    intensidad: Optional[float] = 5.0
    fuente: Optional[str] = None
    fecha: Optional[date] = None
    notas: Optional[str] = None

@router.get("/{project_id}")
def list_emotions(project_id: int, db: Session = Depends(get_db)):
    items = db.query(Emotion).filter(Emotion.project_id == project_id).order_by(Emotion.fecha.desc()).all()
    return [{"id": e.id, "tipo": e.tipo, "intensidad": e.intensidad, "fuente": e.fuente,
             "fecha": str(e.fecha) if e.fecha else None, "notas": e.notas} for e in items]

@router.get("/{project_id}/radar")
def radar_data(project_id: int, db: Session = Depends(get_db)):
    TIPOS = ["ira", "miedo", "frustracion", "esperanza", "desconfianza", "orgullo"]
    result = []
    for tipo in TIPOS:
        avg = db.query(func.avg(Emotion.intensidad)).filter(
            Emotion.project_id == project_id, Emotion.tipo == tipo
        ).scalar()
        result.append({"tipo": tipo, "valor": round(float(avg), 1) if avg else 0})
    return result

@router.post("/")
def create_emotion(data: EmotionSchema, db: Session = Depends(get_db)):
    item = Emotion(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return {"id": item.id}

@router.put("/{item_id}")
def update_emotion(item_id: int, data: EmotionSchema, db: Session = Depends(get_db)):
    item = db.query(Emotion).filter(Emotion.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit(); return {"ok": True}

@router.delete("/{item_id}")
def delete_emotion(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Emotion).filter(Emotion.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    db.delete(item); db.commit(); return {"ok": True}
