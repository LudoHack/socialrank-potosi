from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db
from models.language_code import LanguageCode

router = APIRouter()

class LangSchema(BaseModel):
    project_id: int
    termino: str
    tipo: Optional[str] = "frase"
    frecuencia: Optional[int] = 1
    contexto: Optional[str] = None
    fecha_deteccion: Optional[date] = None
    funcion_cultural: Optional[str] = None      # indecision|desconfianza|activacion|espanto|economia|gestion|emocional|identidad
    impacto_voto_blando: Optional[str] = None   # activa|neutral|espanta

def _serialize(l: LanguageCode) -> dict:
    return {
        "id": l.id,
        "termino": l.termino,
        "tipo": l.tipo,
        "frecuencia": l.frecuencia,
        "contexto": l.contexto,
        "fecha_deteccion": str(l.fecha_deteccion) if l.fecha_deteccion else None,
        "funcion_cultural": l.funcion_cultural,
        "impacto_voto_blando": l.impacto_voto_blando,
    }

@router.get("/{project_id}")
def list_language(project_id: int, db: Session = Depends(get_db)):
    items = db.query(LanguageCode).filter(
        LanguageCode.project_id == project_id
    ).order_by(LanguageCode.frecuencia.desc()).all()
    return [_serialize(l) for l in items]

@router.post("/")
def create_language(data: LangSchema, db: Session = Depends(get_db)):
    item = LanguageCode(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return {"id": item.id}

@router.put("/{item_id}")
def update_language(item_id: int, data: LangSchema, db: Session = Depends(get_db)):
    item = db.query(LanguageCode).filter(LanguageCode.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit(); return {"ok": True}

@router.delete("/{item_id}")
def delete_language(item_id: int, db: Session = Depends(get_db)):
    item = db.query(LanguageCode).filter(LanguageCode.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    db.delete(item); db.commit(); return {"ok": True}
