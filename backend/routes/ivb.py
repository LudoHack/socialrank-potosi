"""
IVB — Indicador de Voto Blando
Índice compuesto 0-100 construido a partir de 5 sub-indicadores.

Componentes y pesos:
  IIN — Índice de Indefinición Narrativa     25%
  IEB — Índice Emocional Blando              20%
  INM — Índice de No-Militancia              20%
  IVN — Índice de Volatilidad Narrativa      20%
  ICC — Índice de Confianza Condicional      15%
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import statistics
from database import get_db
from models.narrative import Narrative
from models.emotion import Emotion
from models.language_code import LanguageCode
from models.community import Community
from models.risk import Risk
from models.archetype import Archetype

router = APIRouter()

# ── Vocabulario de indecisión ──────────────────────────────────────────────────
_INDECISION = [
    "todavía", "estoy viendo", "no me convence", "último momento", "capaz",
    "depende", "aún no", "sin decidir", "ninguno", "todos tienen",
    "no hay por quién", "puede definirlo", "indeciso", "blando",
    "a último", "viendo opciones", "evaluando",
]

_CONDITIONAL = [
    "si cumple", "por ahora", "me gusta pero", "a ver si",
    "voto si", "si hace", "todavía viendo", "con reservas",
]

def _has_kw(text: str, keywords: list) -> bool:
    t = (text or "").lower()
    return any(k in t for k in keywords)


# ── Sub-índices ────────────────────────────────────────────────────────────────

def _iin(narratives, language) -> float:
    """Índice de Indefinición Narrativa (0-100)"""
    n_score = 0.0
    if narratives:
        hits = sum(1 for n in narratives if _has_kw(n.texto, _INDECISION))
        n_score = hits / len(narratives) * 100

    l_score = 0.0
    total_freq = sum(lc.frecuencia or 0 for lc in language)
    if total_freq > 0:
        hit_freq = sum(
            lc.frecuencia or 0 for lc in language
            if _has_kw(lc.termino, _INDECISION) or _has_kw(lc.contexto, _INDECISION)
        )
        l_score = hit_freq / total_freq * 100

    raw = n_score * 0.5 + l_score * 0.5
    # Amplify: a 20 % raw hit rate maps to ~50 in the index
    return min(100.0, raw * 2.5)


def _ieb(emotions) -> float:
    """Índice Emocional Blando (0-100)"""
    if not emotions:
        return 50.0

    soft_types = {"desconfianza", "frustracion", "miedo"}
    hard_types = {"ira", "orgullo"}

    soft_vals = [e.intensidad for e in emotions if e.tipo in soft_types]
    hard_vals = [e.intensidad for e in emotions if e.tipo in hard_types]
    hope_vals  = [e.intensidad for e in emotions if e.tipo == "esperanza"]

    soft_avg = statistics.mean(soft_vals) if soft_vals else 5.0
    hard_avg = statistics.mean(hard_vals) if hard_vals else 5.0

    # Low / moderate esperanza reinforces blando (esperanza ≤ 6)
    hope_low = [v for v in hope_vals if v <= 6]
    hope_bonus = (statistics.mean(hope_low) / 10) * 15 if hope_low else 0

    # Normalize: soft > hard → high IEB
    base = ((soft_avg - hard_avg + 10) / 20) * 80   # 0–80
    return min(100.0, max(0.0, base + hope_bonus))


def _inm(communities, archetypes) -> float:
    """Índice de No-Militancia (0-100)"""
    TIPO_W = {"silencioso": 100, "amplificador": 65, "activo": 35, "polarizado": 5}

    if communities:
        total_w, wsum = 0, 0
        for c in communities:
            w = (c.tamanio_estimado or 100) * (c.influencia or 5)
            total_w += w
            wsum += w * TIPO_W.get(c.tipo, 50)
        inm_comm = wsum / total_w if total_w else 50.0
    else:
        inm_comm = 50.0

    BLANDO_EMOC = {"desconfianza", "miedo", "frustracion"}
    if archetypes:
        total_p = sum(a.peso_relativo or 0 for a in archetypes) or 1
        blando_p = sum(a.peso_relativo or 0 for a in archetypes
                       if a.emocion_dominante in BLANDO_EMOC)
        inm_arch = blando_p / total_p * 100
    else:
        inm_arch = 50.0

    return inm_comm * 0.6 + inm_arch * 0.4


def _ivn(narratives, risks) -> float:
    """Índice de Volatilidad Narrativa (0-100)"""
    if narratives:
        n_total = len(narratives)
        n_vol = sum(1 for n in narratives if n.tipo in ("emergente", "contrarrelato"))
        div_score = n_vol / n_total * 100
    else:
        div_score = 50.0

    if risks:
        avg_vel = statistics.mean([r.velocidad_crecimiento or 3 for r in risks])
        vel_score = (avg_vel / 5) * 100
    else:
        vel_score = 50.0

    return div_score * 0.5 + vel_score * 0.5


def _icc(narratives, emotions, language) -> float:
    """Índice de Confianza Condicional (0-100)"""
    # Narrativas emergentes de peso moderado (apoyo no consolidado)
    if narratives:
        cond_n = [n for n in narratives if n.tipo == "emergente" and 3 <= (n.peso or 0) <= 7]
        n_score = len(cond_n) / len(narratives) * 100
    else:
        n_score = 0.0

    # Esperanza baja-moderada = expectativa con reservas
    hope = [e for e in emotions if e.tipo == "esperanza"]
    if hope:
        cond_hope = [e for e in hope if 3 <= e.intensidad <= 7]
        h_score = len(cond_hope) / len(hope) * 100
    else:
        h_score = 0.0

    # Lenguaje condicional
    total_freq = sum(lc.frecuencia or 0 for lc in language) or 1
    cond_freq = sum(
        lc.frecuencia or 0 for lc in language
        if _has_kw(lc.termino, _CONDITIONAL) or _has_kw(lc.contexto, _CONDITIONAL)
    )
    l_score = cond_freq / total_freq * 100

    raw = n_score * 0.5 + h_score * 0.3 + l_score * 0.2
    return min(100.0, raw + 15)   # baseline +15 (ICC siempre tiene algo)


# ── Estado e interpretación ────────────────────────────────────────────────────

def _estado(score: float) -> dict:
    if score <= 30:
        return {"label": "Voto duro predominante",           "color": "#56c596", "nivel": "bajo",    "zona": "0–30"}
    elif score <= 55:
        return {"label": "Voto semi-blando — activable",     "color": "#f7c948", "nivel": "medio",   "zona": "31–55"}
    elif score <= 75:
        return {"label": "Voto blando alto — zona crítica",  "color": "#f7964a", "nivel": "alto",    "zona": "56–75"}
    else:
        return {"label": "Voto blando extremo — riesgo fuga","color": "#f76c6c", "nivel": "critico", "zona": "76–100"}


def _alertas(ivb, iin, ieb, inm, ivn, icc) -> list:
    result = []
    if ivb > 75:
        result.append({"tipo": "critico", "icono": "🚨",
                        "mensaje": "IVB crítico — alto riesgo de abstención o voto castigo"})
    if ivb > 70 and ieb < 40:
        result.append({"tipo": "critico", "icono": "🚨",
                        "mensaje": "IVB alto con ira en ascenso — posible fuga hacia candidato opositor agresivo"})
    if ivn > 70:
        result.append({"tipo": "warning", "icono": "⚡",
                        "mensaje": "Alta volatilidad — cualquier error discursivo puede mover el voto en <72h"})
    if ivb > 55 and icc > 60:
        result.append({"tipo": "oportunidad", "icono": "✅",
                        "mensaje": "Señales de confianza condicional — ventana de activación abierta"})
    if ivb > 50 and iin > 60:
        result.append({"tipo": "warning", "icono": "👁️",
                        "mensaje": "Alta indefinición narrativa — el voto blando aún no tiene candidato propio"})
    return result


def _recomendacion(ivb: float, ieb: float, ivn: float) -> str:
    if ivb >= 56:
        return (
            "El principal campo de disputa no está entre bloques duros, sino sobre un voto "
            "blando amplio, volátil y altamente sensible a errores discursivos. "
            "Priorizar mensajes de certeza, orden y credibilidad. Evitar polarización, "
            "promesas totales y tono agresivo."
        )
    elif ivb >= 31:
        return (
            "Existe un segmento semi-blando activable con propuestas concretas y creíbles. "
            "Mensajes que combinen empatía con soluciones medibles pueden consolidar adhesión. "
            "Evitar polarización innecesaria."
        )
    else:
        return (
            "El electorado tiende a posiciones consolidadas. La disputa principal es entre "
            "bloques. Enfocar energía en activación de la base propia y no alejar al votante "
            "semi-blando con mensajes extremos."
        )


# ── Endpoint principal ─────────────────────────────────────────────────────────

@router.get("/{project_id}")
def get_ivb(project_id: int, db: Session = Depends(get_db)):
    narratives  = db.query(Narrative).filter(Narrative.project_id == project_id).all()
    emotions    = db.query(Emotion).filter(Emotion.project_id == project_id).all()
    language    = db.query(LanguageCode).filter(LanguageCode.project_id == project_id).all()
    communities = db.query(Community).filter(Community.project_id == project_id).all()
    risks       = db.query(Risk).filter(Risk.project_id == project_id, Risk.activo == True).all()
    archetypes  = db.query(Archetype).filter(Archetype.project_id == project_id).all()

    iin_v = _iin(narratives, language)
    ieb_v = _ieb(emotions)
    inm_v = _inm(communities, archetypes)
    ivn_v = _ivn(narratives, risks)
    icc_v = _icc(narratives, emotions, language)

    ivb = round(
        0.25 * iin_v + 0.20 * ieb_v + 0.20 * inm_v + 0.20 * ivn_v + 0.15 * icc_v,
        1
    )

    estado = _estado(ivb)

    componentes = {
        "IIN": {
            "valor": round(iin_v, 1), "peso": 25,
            "nombre": "Indefinición Narrativa",
            "descripcion": "Discursos de no-decisión y lenguaje de indecisión detectados",
            "icono": "🔍",
        },
        "IEB": {
            "valor": round(ieb_v, 1), "peso": 20,
            "nombre": "Emocional Blando",
            "descripcion": "Predominio de desconfianza y frustración sobre ira y orgullo",
            "icono": "🎭",
        },
        "INM": {
            "valor": round(inm_v, 1), "peso": 20,
            "nombre": "No-Militancia",
            "descripcion": "Comunidades y arquetipos que observan sin defender activamente",
            "icono": "👁️",
        },
        "IVN": {
            "valor": round(ivn_v, 1), "peso": 20,
            "nombre": "Volatilidad Narrativa",
            "descripcion": "Diversidad narrativa y velocidad de cambio ante micro-eventos",
            "icono": "⚡",
        },
        "ICC": {
            "valor": round(icc_v, 1), "peso": 15,
            "nombre": "Confianza Condicional",
            "descripcion": "Apoyo reversible, expectativa con reservas y lenguaje condicional",
            "icono": "🤝",
        },
    }

    return {
        "ivb": ivb,
        "estado": estado,
        "componentes": componentes,
        "alertas": _alertas(ivb, iin_v, ieb_v, inm_v, ivn_v, icc_v),
        "recomendacion": _recomendacion(ivb, ieb_v, ivn_v),
        "tabla_interpretacion": [
            {"rango": "0 – 30",   "estado": "Voto duro",            "lectura": "Poco influenciable",                "color": "#56c596"},
            {"rango": "31 – 55",  "estado": "Voto semi-blando",     "lectura": "Puede activarse o perderse",        "color": "#f7c948"},
            {"rango": "56 – 75",  "estado": "Voto blando alto",     "lectura": "Zona crítica de disputa",           "color": "#f7964a"},
            {"rango": "76 – 100", "estado": "Voto blando extremo",  "lectura": "Riesgo alto de abstención/castigo", "color": "#f76c6c"},
        ],
        "meta": {
            "narrativas": len(narratives), "emociones": len(emotions),
            "lenguaje": len(language), "comunidades": len(communities),
        },
    }
