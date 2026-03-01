from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models.project import Project
from models.archetype import Archetype
from models.emotion import Emotion
from models.narrative import Narrative
from models.risk import Risk
from models.simulation import Simulation
from services.claude_service import simulate_message, generate_recommendations

router = APIRouter()

class SimulateRequest(BaseModel):
    project_id: int
    mensaje: str

class RecommendRequest(BaseModel):
    project_id: int

def build_project_context(project_id: int, db: Session) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    arquetipos = db.query(Archetype).filter(Archetype.project_id == project_id).all()
    emociones = db.query(Emotion).filter(Emotion.project_id == project_id).limit(30).all()
    narrativas = db.query(Narrative).filter(Narrative.project_id == project_id).order_by(Narrative.peso.desc()).limit(10).all()
    riesgos = db.query(Risk).filter(Risk.project_id == project_id, Risk.activo == True, Risk.nivel == "rojo").all()
    return {
        "proyecto": project.nombre if project else "Desconocido",
        "contexto_pais": project.contexto_pais if project else "",
        "arquetipos": [{"nombre": a.nombre, "peso": a.peso_relativo, "emocion": a.emocion_dominante,
                        "canales": a.canales, "valores": a.valores_clave, "miedos": a.miedos} for a in arquetipos],
        "emociones": [{"tipo": e.tipo, "intensidad": e.intensidad, "fuente": e.fuente} for e in emociones],
        "narrativas_top": [{"texto": n.texto, "tipo": n.tipo, "peso": n.peso} for n in narrativas],
        "riesgos_criticos": [{"tema": r.tema, "nivel": r.nivel} for r in riesgos],
    }

@router.post("/simulate")
def simulate(req: SimulateRequest, db: Session = Depends(get_db)):
    try:
        context = build_project_context(req.project_id, db)
        result = simulate_message(req.mensaje, context)
        sim = Simulation(project_id=req.project_id, mensaje_propuesto=req.mensaje, resultado_json=result)
        db.add(sim); db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend")
def recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    try:
        context = build_project_context(req.project_id, db)
        result = generate_recommendations(context)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/simulations/{project_id}")
def list_simulations(project_id: int, db: Session = Depends(get_db)):
    items = db.query(Simulation).filter(Simulation.project_id == project_id).order_by(Simulation.created_at.desc()).limit(20).all()
    return [{"id": s.id, "mensaje": s.mensaje_propuesto, "resultado": s.resultado_json,
             "fecha": str(s.created_at)} for s in items]
