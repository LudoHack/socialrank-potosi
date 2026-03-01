from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.narrative import Narrative
from models.emotion import Emotion
from models.risk import Risk

router = APIRouter()

@router.get("/{project_id}")
def get_evolution(project_id: int, db: Session = Depends(get_db)):
    # Narrativas por mes
    _mes_n = func.strftime('%Y-%m', Narrative.fecha_deteccion)
    narrativas_mes = db.query(
        _mes_n.label("mes"),
        func.count(Narrative.id).label("count")
    ).filter(
        Narrative.project_id == project_id,
        Narrative.fecha_deteccion != None
    ).group_by(_mes_n).order_by(_mes_n).all()

    # Emociones promedio por mes
    _mes_e = func.strftime('%Y-%m', Emotion.fecha)
    emociones_mes = db.query(
        _mes_e.label("mes"),
        Emotion.tipo,
        func.avg(Emotion.intensidad).label("avg")
    ).filter(
        Emotion.project_id == project_id,
        Emotion.fecha != None
    ).group_by(_mes_e, Emotion.tipo).order_by(_mes_e).all()

    # Riesgos por mes detectados
    _mes_r = func.strftime('%Y-%m', Risk.fecha_deteccion)
    riesgos_mes = db.query(
        _mes_r.label("mes"),
        Risk.nivel,
        func.count(Risk.id).label("count")
    ).filter(
        Risk.project_id == project_id,
        Risk.fecha_deteccion != None
    ).group_by(_mes_r, Risk.nivel).order_by(_mes_r).all()

    return {
        "narrativas_por_mes": [{"mes": r.mes, "count": r.count} for r in narrativas_mes],
        "emociones_por_mes":  [{"mes": r.mes, "tipo": r.tipo, "avg": round(float(r.avg), 1)} for r in emociones_mes],
        "riesgos_por_mes":    [{"mes": r.mes, "nivel": r.nivel, "count": r.count} for r in riesgos_mes],
    }
