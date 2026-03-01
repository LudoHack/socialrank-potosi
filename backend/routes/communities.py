from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from database import get_db
from models.community import Community

router = APIRouter()

class CommunitySchema(BaseModel):
    project_id: int
    plataforma: Optional[str] = None
    nombre_grupo: Optional[str] = None
    tipo: Optional[str] = "activo"
    tamanio_estimado: Optional[int] = None
    descripcion: Optional[str] = None
    influencia: Optional[int] = 5

@router.get("/{project_id}")
def list_communities(project_id: int, db: Session = Depends(get_db)):
    items = db.query(Community).filter(Community.project_id == project_id).order_by(Community.influencia.desc()).all()
    return [{"id": c.id, "plataforma": c.plataforma, "nombre_grupo": c.nombre_grupo,
             "tipo": c.tipo, "tamanio_estimado": c.tamanio_estimado,
             "descripcion": c.descripcion, "influencia": c.influencia} for c in items]

@router.post("/")
def create_community(data: CommunitySchema, db: Session = Depends(get_db)):
    item = Community(**data.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return {"id": item.id}

@router.put("/{item_id}")
def update_community(item_id: int, data: CommunitySchema, db: Session = Depends(get_db)):
    item = db.query(Community).filter(Community.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    db.commit(); return {"ok": True}

@router.delete("/{item_id}")
def delete_community(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Community).filter(Community.id == item_id).first()
    if not item: raise HTTPException(404, "No encontrado")
    db.delete(item); db.commit(); return {"ok": True}
