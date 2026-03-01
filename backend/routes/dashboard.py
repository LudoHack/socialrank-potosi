from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.project import Project
from models.narrative import Narrative
from models.emotion import Emotion
from models.archetype import Archetype
from models.language_code import LanguageCode
from models.community import Community
from models.risk import Risk

router = APIRouter()

@router.get("/{project_id}")
def get_dashboard(project_id: int, db: Session = Depends(get_db)):
    p = db.query(Project).filter(Project.id == project_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    # Conteos generales
    total_narrativas  = db.query(func.count(Narrative.id)).filter(Narrative.project_id == project_id).scalar()
    total_emociones   = db.query(func.count(Emotion.id)).filter(Emotion.project_id == project_id).scalar()
    total_arquetipos  = db.query(func.count(Archetype.id)).filter(Archetype.project_id == project_id).scalar()
    total_lenguaje    = db.query(func.count(LanguageCode.id)).filter(LanguageCode.project_id == project_id).scalar()
    total_comunidades = db.query(func.count(Community.id)).filter(Community.project_id == project_id).scalar()
    riesgos_rojos     = db.query(func.count(Risk.id)).filter(Risk.project_id == project_id, Risk.nivel == "rojo", Risk.activo == True).scalar()
    riesgos_amarillos = db.query(func.count(Risk.id)).filter(Risk.project_id == project_id, Risk.nivel == "amarillo", Risk.activo == True).scalar()
    riesgos_verdes    = db.query(func.count(Risk.id)).filter(Risk.project_id == project_id, Risk.nivel == "verde", Risk.activo == True).scalar()

    # Emociones promedio por tipo
    emociones_avg = db.query(
        Emotion.tipo,
        func.avg(Emotion.intensidad).label("avg"),
        func.count(Emotion.id).label("count")
    ).filter(Emotion.project_id == project_id).group_by(Emotion.tipo).all()

    # Narrativas por tipo
    narrativas_tipo = db.query(
        Narrative.tipo,
        func.count(Narrative.id).label("count")
    ).filter(Narrative.project_id == project_id).group_by(Narrative.tipo).all()

    # Arquetipos top 5
    arquetipos_top = db.query(Archetype).filter(
        Archetype.project_id == project_id
    ).order_by(Archetype.peso_relativo.desc()).limit(5).all()

    # Riesgos activos críticos
    riesgos_criticos = db.query(Risk).filter(
        Risk.project_id == project_id,
        Risk.nivel == "rojo",
        Risk.activo == True
    ).order_by(Risk.velocidad_crecimiento.desc()).limit(5).all()

    return {
        "proyecto": {"id": p.id, "nombre": p.nombre, "cliente": p.cliente, "contexto_pais": p.contexto_pais},
        "totales": {
            "narrativas": total_narrativas,
            "emociones": total_emociones,
            "arquetipos": total_arquetipos,
            "lenguaje": total_lenguaje,
            "comunidades": total_comunidades,
        },
        "riesgos": {"rojo": riesgos_rojos, "amarillo": riesgos_amarillos, "verde": riesgos_verdes},
        "emociones_radar": [{"tipo": e.tipo, "avg": round(float(e.avg), 1), "count": e.count} for e in emociones_avg],
        "narrativas_por_tipo": [{"tipo": n.tipo or "sin tipo", "count": n.count} for n in narrativas_tipo],
        "arquetipos_top": [{"nombre": a.nombre, "peso": a.peso_relativo, "emocion": a.emocion_dominante} for a in arquetipos_top],
        "riesgos_criticos": [{"tema": r.tema, "nivel": r.nivel, "velocidad": r.velocidad_crecimiento} for r in riesgos_criticos],
    }
