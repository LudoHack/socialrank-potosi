from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from database import get_db
from models.archetype import Archetype

router = APIRouter()

class ArchetypeSchema(BaseModel):
    project_id: int
    nombre: str
    descripcion: Optional[str] = None
    peso_relativo: Optional[float] = 0.0
    emocion_dominante: Optional[str] = None
    canales: Optional[List[str]] = []
    valores_clave: Optional[str] = None
    miedos: Optional[str] = None

@router.get("/{project_id}")
def list_archetypes(project_id: int, db: Session = Depends(get_db)):
    items = db.query(Archetype).filter(Archetype.project_id == project_id).order_by(Archetype.peso_relativo.desc()).all()
    return [{"id": a.id, "nombre": a.nombre, "descripcion": a.descripcion,
             "peso_relativo": a.peso_relativo, "emocion_dominante": a.emocion_dominante,
             "canales": a.canales or [], "valores_clave": a.valores_clave, "miedos": a.miedos} for a in items]

@router.post("/")
def create_archetype(data: ArchetypeSchema, db: Session = Depends(get_db)):
    item = Archetype(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return {"id": item.id}

@router.put("/{item_id}")
def update_archetype(item_id: int, data: ArchetypeSchema, db: Session = Depends(get_db)):
    item = db.query(Archetype).filter(Archetype.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit(); return {"ok": True}

@router.delete("/{item_id}")
def delete_archetype(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Archetype).filter(Archetype.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    db.delete(item); db.commit(); return {"ok": True}
