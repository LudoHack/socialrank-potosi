from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from typing import Optional
from datetime import date
from database import get_db
from models.project import Project
from models.narrative import Narrative
from models.emotion import Emotion
from models.archetype import Archetype
from models.risk import Risk

router = APIRouter()

class ProjectCreate(BaseModel):
    nombre: str
    cliente: Optional[str] = None
    contexto_pais: Optional[str] = None
    fecha_inicio: Optional[date] = None
    descripcion: Optional[str] = None

class ProjectUpdate(ProjectCreate):
    activo: Optional[bool] = None

@router.get("/")
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).order_by(Project.created_at.desc()).all()
    result = []
    for p in projects:
        result.append({
            "id": p.id,
            "nombre": p.nombre,
            "cliente": p.cliente,
            "contexto_pais": p.contexto_pais,
            "fecha_inicio": str(p.fecha_inicio) if p.fecha_inicio else None,
            "descripcion": p.descripcion,
            "activo": p.activo,
            "created_at": str(p.created_at),
            "stats": {
                "narrativas": db.query(func.count(Narrative.id)).filter(Narrative.project_id == p.id).scalar(),
                "emociones": db.query(func.count(Emotion.id)).filter(Emotion.project_id == p.id).scalar(),
                "arquetipos": db.query(func.count(Archetype.id)).filter(Archetype.project_id == p.id).scalar(),
                "riesgos_activos": db.query(func.count(Risk.id)).filter(Risk.project_id == p.id, Risk.activo == True).scalar(),
            }
        })
    return result

@router.post("/")
def create_project(data: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**data.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "nombre": project.nombre, "activo": project.activo}

@router.get("/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return p

@router.put("/{project_id}")
def update_project(project_id: int, data: ProjectUpdate, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    db.delete(p)
    db.commit()
    return {"ok": True}
