"""
seed_lenguaje.py — Carga todos los términos culturales del voto blando en la DB.
Los términos nuevos se agregan; si ya existe el mismo termino+project no se duplica.
"""
import sys
sys.path.insert(0, 'D:/etnografica/backend')

from datetime import date
from database import SessionLocal
from models.language_code import LanguageCode

PID = 1  # project_id de Santa Cruz 2026

TERMS = [
    # ── 1. Indecisión / Voto blando explícito ─────────────────────────────
    {"termino": "todavía",          "tipo": "termino", "frecuencia": 347, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-10", "contexto": "Indecisión activa explícita. Señal núcleo del IVB."},
    {"termino": "viendo",           "tipo": "termino", "frecuencia": 201, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-10", "contexto": "Expresión de espera evaluativa pre-electoral."},
    {"termino": "comparando",       "tipo": "termino", "frecuencia": 218, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-11", "contexto": "El elector activo que evalúa candidatos sin decidir."},
    {"termino": "no sé",            "tipo": "frase",   "frecuencia": 298, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-11", "contexto": "Voto blando puro. Alta frecuencia en redes."},
    {"termino": "depende",          "tipo": "termino", "frecuencia": 276, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-11", "contexto": "Condicionamiento electoral. Elector persuadible."},
    {"termino": "último momento",   "tipo": "frase",   "frecuencia": 189, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-12", "contexto": "Decisión tardía. Perfil altamente influenciable."},
    {"termino": "indeciso",         "tipo": "termino", "frecuencia": 167, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-12", "contexto": "Autodeclaración de voto blando."},
    {"termino": "ninguno convence", "tipo": "frase",   "frecuencia": 143, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-12", "contexto": "Frustración con la oferta electoral. Activable."},
    {"termino": "ver qué pasa",     "tipo": "frase",   "frecuencia": 154, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-13", "contexto": "Postura expectante típica del voto blando."},
    {"termino": "esperando",        "tipo": "termino", "frecuencia": 131, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-13", "contexto": "Espera de señales para decidir."},
    {"termino": "evaluando",        "tipo": "termino", "frecuencia": 112, "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-13", "contexto": "Proceso activo de decisión no concluido."},
    {"termino": "por ahora",        "tipo": "frase",   "frecuencia": 98,  "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-14", "contexto": "Apoyo condicional. Volátil."},
    {"termino": "capaz",            "tipo": "termino", "frecuencia": 76,  "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-14", "contexto": "Forma regional de 'tal vez'. Incertidumbre suave."},
    {"termino": "tal vez",          "tipo": "frase",   "frecuencia": 87,  "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-14", "contexto": "Probabilidad baja de compromiso firme."},
    {"termino": "falta ver",        "tipo": "frase",   "frecuencia": 62,  "funcion_cultural": "indecision", "impacto_voto_blando": "activa",  "fecha": "2026-02-14", "contexto": "Evaluación incompleta. Elector aún formando opinión."},

    # ── 2. Desconfianza suave ──────────────────────────────────────────────
    {"termino": "no convence",      "tipo": "frase",   "frecuencia": 287, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-12", "contexto": "Rechazo soft. Alta frecuencia. Mueve IVB."},
    {"termino": "más de lo mismo",  "tipo": "frase",   "frecuencia": 256, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-12", "contexto": "Hartazgo con la clase política en general."},
    {"termino": "prometer",         "tipo": "termino", "frecuencia": 233, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-12", "contexto": "Asociado a incumplimiento histórico."},
    {"termino": "discurso",         "tipo": "termino", "frecuencia": 198, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-13", "contexto": "Desconexión entre palabras y hechos."},
    {"termino": "humo",             "tipo": "termino", "frecuencia": 109, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-13", "contexto": "Expresión coloquial de falsedad o engaño político."},
    {"termino": "palabras",         "tipo": "termino", "frecuencia": 121, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-13", "contexto": "Sólo palabras, no hechos. Crítica recurrente."},
    {"termino": "cuentos",          "tipo": "termino", "frecuencia": 132, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-13", "contexto": "Expresión de incredulidad ante propuestas."},
    {"termino": "siempre igual",    "tipo": "frase",   "frecuencia": 176, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-14", "contexto": "Sensación de ciclicidad política sin cambio real."},
    {"termino": "políticos",        "tipo": "termino", "frecuencia": 187, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-14", "contexto": "Término paraguas de desconfianza institucional."},
    {"termino": "marketing",        "tipo": "termino", "frecuencia": 154, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-14", "contexto": "Campaña percibida como artificiosa o publicitaria."},
    {"termino": "show",             "tipo": "termino", "frecuencia": 143, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Espectacularización de la política. Rechazo de autenticidad."},
    {"termino": "promesas",         "tipo": "termino", "frecuencia": 218, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Símbolo de incumplimiento electoral histórico."},
    {"termino": "dudar",            "tipo": "termino", "frecuencia": 89,  "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Expresión directa de duda sobre candidatos."},
    {"termino": "ver para creer",   "tipo": "frase",   "frecuencia": 312, "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Alta frecuencia. Escepticismo pragmático. Monitor constante."},
    {"termino": "desconfiar",       "tipo": "termino", "frecuencia": 76,  "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta", "fecha": "2026-02-16", "contexto": "Desconfianza explícita. Perfil difícil de persuadir."},

    # ── 3. Activación potencial ────────────────────────────────────────────
    {"termino": "concreto",         "tipo": "termino", "frecuencia": 321, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-14", "contexto": "Palabra gatillo de activación. Alto IVB positivo."},
    {"termino": "claro",            "tipo": "termino", "frecuencia": 265, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-14", "contexto": "Claridad del mensaje activa al elector blando."},
    {"termino": "simple",           "tipo": "termino", "frecuencia": 243, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-14", "contexto": "Mensaje simple = confianza. Activa decisión de voto."},
    {"termino": "sentido común",    "tipo": "frase",   "frecuencia": 132, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-15", "contexto": "Validación del candidato como 'gente como uno'."},
    {"termino": "solución",         "tipo": "termino", "frecuencia": 198, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-15", "contexto": "Demanda central del elector pragmático."},
    {"termino": "práctico",         "tipo": "termino", "frecuencia": 178, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-15", "contexto": "Pragmatismo como valor electoral."},
    {"termino": "directo",          "tipo": "termino", "frecuencia": 167, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-15", "contexto": "Comunicación directa activa al voto blando."},
    {"termino": "resultados",       "tipo": "termino", "frecuencia": 298, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-16", "contexto": "Evidencia de gestión. Activa fuertemente. Monitor."},
    {"termino": "cumplir",          "tipo": "termino", "frecuencia": 231, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-16", "contexto": "Contrasta con 'promesas'. Alta activación."},
    {"termino": "hacer",            "tipo": "termino", "frecuencia": 156, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-16", "contexto": "Acción vs. discurso. Activa perfil pragmático."},
    {"termino": "trabajar",         "tipo": "termino", "frecuencia": 219, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-16", "contexto": "Valor de laboriosidad. Activa identidad cruceña."},
    {"termino": "básico",           "tipo": "termino", "frecuencia": 143, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Reclamo de lo elemental. Activa indignación productiva."},
    {"termino": "responsable",      "tipo": "termino", "frecuencia": 121, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Atributo valorado. Contrasta con desconfianza."},
    {"termino": "serio",            "tipo": "termino", "frecuencia": 109, "funcion_cultural": "activacion", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Credibilidad. Activa al elector desconfiado moderado."},

    # ── 4. Espanto del voto blando (ALERTA: sube el IVB) ──────────────────
    {"termino": "pelea",            "tipo": "termino", "frecuencia": 276, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-13", "contexto": "ALERTA: conflicto político espanta al voto blando."},
    {"termino": "ataque",           "tipo": "termino", "frecuencia": 176, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-13", "contexto": "Campaña negativa activa el espanto."},
    {"termino": "insulto",          "tipo": "termino", "frecuencia": 243, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-13", "contexto": "ALERTA: insultos entre candidatos elevan IVB."},
    {"termino": "enemigo",          "tipo": "termino", "frecuencia": 231, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-14", "contexto": "ALERTA: narrativa de enemistad aleja al blando."},
    {"termino": "odio",             "tipo": "termino", "frecuencia": 154, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-14", "contexto": "Polarización extrema. Repele al elector moderado."},
    {"termino": "radical",          "tipo": "termino", "frecuencia": 218, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-14", "contexto": "ALERTA: percepción de extremismo sube IVB."},
    {"termino": "extremo",          "tipo": "termino", "frecuencia": 165, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-14", "contexto": "Junto a 'radical', activa el espanto del voto blando."},
    {"termino": "ideología",        "tipo": "termino", "frecuencia": 143, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Para el elector pragmático, 'ideología' = alarma."},
    {"termino": "confrontación",    "tipo": "termino", "frecuencia": 187, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Conflicto explícito entre actores políticos."},
    {"termino": "imponer",          "tipo": "termino", "frecuencia": 132, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Percepción de autoritarismo. Espanta al moderado."},
    {"termino": "guerra",           "tipo": "termino", "frecuencia": 121, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Metáfora bélica repelente para el voto blando."},
    {"termino": "mano dura",        "tipo": "frase",   "frecuencia": 209, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-16", "contexto": "ALERTA: percibido como extremismo. Monitor continuo."},
    {"termino": "castigo",          "tipo": "termino", "frecuencia": 89,  "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-16", "contexto": "Retórica punitiva aleja al elector moderado."},
    {"termino": "autoritario",      "tipo": "termino", "frecuencia": 109, "funcion_cultural": "espanto", "impacto_voto_blando": "espanta", "fecha": "2026-02-16", "contexto": "Acusación de autoritarismo. Alta toxicidad electoral."},

    # ── 5. Economía cotidiana ──────────────────────────────────────────────
    {"termino": "precios",          "tipo": "termino", "frecuencia": 412, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-08", "contexto": "Gatillo #1. Máxima frecuencia en toda la nube."},
    {"termino": "caro",             "tipo": "termino", "frecuencia": 356, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-08", "contexto": "Reclamo cotidiano. Activa voto protesta y demanda."},
    {"termino": "inflación",        "tipo": "termino", "frecuencia": 298, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-08", "contexto": "Contexto macroeconómico traducido a lo cotidiano."},
    {"termino": "alcanza",          "tipo": "termino", "frecuencia": 231, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-09", "contexto": "'No alcanza'. Angustia económica doméstica."},
    {"termino": "bolsillo",         "tipo": "termino", "frecuencia": 387, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-09", "contexto": "Metonimia de economía personal. Alta activación."},
    {"termino": "plata",            "tipo": "termino", "frecuencia": 334, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-09", "contexto": "Dinero en lenguaje coloquial. Muy frecuente."},
    {"termino": "sueldo",           "tipo": "termino", "frecuencia": 265, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-09", "contexto": "Ingreso laboral. Central en el debate electoral."},
    {"termino": "trabajo",          "tipo": "termino", "frecuencia": 287, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-10", "contexto": "Empleo como demanda central del voto pragmático."},
    {"termino": "empleo",           "tipo": "termino", "frecuencia": 243, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-10", "contexto": "Sinónimo formal de trabajo. Alta frecuencia."},
    {"termino": "crisis",           "tipo": "termino", "frecuencia": 312, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-10", "contexto": "Estado de emergencia económica subjetiva."},
    {"termino": "dólares",          "tipo": "termino", "frecuencia": 218, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-10", "contexto": "Contexto de dolarización informal y economía binaria."},
    {"termino": "gastos",           "tipo": "termino", "frecuencia": 154, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-11", "contexto": "Presión de gastos del hogar. Activador emocional."},
    {"termino": "mercado",          "tipo": "termino", "frecuencia": 176, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-11", "contexto": "El mercado como espacio de preocupación cotidiana."},
    {"termino": "pagar",            "tipo": "termino", "frecuencia": 198, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-11", "contexto": "Obligaciones económicas. Angustia cotidiana."},
    {"termino": "sobrevivir",       "tipo": "termino", "frecuencia": 132, "funcion_cultural": "economia", "impacto_voto_blando": "activa", "fecha": "2026-02-12", "contexto": "Expresión máxima de presión económica subjetiva."},

    # ── 6. Gestión y vida diaria (municipal) ──────────────────────────────
    {"termino": "basura",           "tipo": "termino", "frecuencia": 276, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-11", "contexto": "Reclamo urbano #1. Muy frecuente en quejas barriales."},
    {"termino": "baches",           "tipo": "termino", "frecuencia": 232, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-11", "contexto": "Infraestructura vial. Reclamo cotidiano."},
    {"termino": "calles",           "tipo": "termino", "frecuencia": 218, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-11", "contexto": "Estado de calles como termómetro de gestión."},
    {"termino": "luz",              "tipo": "termino", "frecuencia": 154, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-12", "contexto": "Servicio básico. Cortes = frustración electoral."},
    {"termino": "agua",             "tipo": "termino", "frecuencia": 176, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-12", "contexto": "Servicio básico crítico. Alta sensibilidad electoral."},
    {"termino": "transporte",       "tipo": "termino", "frecuencia": 143, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-12", "contexto": "Movilidad urbana. Impacto diario en votantes."},
    {"termino": "seguridad",        "tipo": "termino", "frecuencia": 298, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-12", "contexto": "Demanda urbana central. Alta frecuencia y emoción."},
    {"termino": "barrio",           "tipo": "termino", "frecuencia": 209, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-13", "contexto": "Unidad territorial de la demanda ciudadana."},
    {"termino": "vecinos",          "tipo": "termino", "frecuencia": 165, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-13", "contexto": "Red social y política a nivel barrial."},
    {"termino": "orden urbano",     "tipo": "frase",   "frecuencia": 254, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-13", "contexto": "Demanda de orden en el espacio público."},
    {"termino": "limpieza",         "tipo": "termino", "frecuencia": 121, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-13", "contexto": "Higiene urbana como indicador de gestión."},
    {"termino": "servicios",        "tipo": "termino", "frecuencia": 187, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-14", "contexto": "Servicios municipales como eje de evaluación."},
    {"termino": "alumbrado",        "tipo": "termino", "frecuencia": 98,  "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-14", "contexto": "Alumbrado público. Seguridad y gestión vinculados."},
    {"termino": "patrullaje",       "tipo": "termino", "frecuencia": 132, "funcion_cultural": "gestion", "impacto_voto_blando": "activa", "fecha": "2026-02-14", "contexto": "Presencia policial. Respuesta a demanda de seguridad."},

    # ── 7. Lenguaje emocional blando (no polarizado) ───────────────────────
    {"termino": "cansancio",        "tipo": "termino", "frecuencia": 221, "funcion_cultural": "emocion", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Fatiga política crónica. Activa el abstencionismo."},
    {"termino": "hartazgo",         "tipo": "termino", "frecuencia": 198, "funcion_cultural": "emocion", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Saturación con la política. Monitor constante."},
    {"termino": "preocupación",     "tipo": "termino", "frecuencia": 121, "funcion_cultural": "emocion", "impacto_voto_blando": "espanta", "fecha": "2026-02-15", "contexto": "Ansiedad electoral difusa. Puede activarse."},
    {"termino": "miedo",            "tipo": "termino", "frecuencia": 265, "funcion_cultural": "emocion", "impacto_voto_blando": "espanta", "fecha": "2026-02-16", "contexto": "Emoción dominante en escenarios de incertidumbre alta."},
    {"termino": "incertidumbre",    "tipo": "termino", "frecuencia": 243, "funcion_cultural": "emocion", "impacto_voto_blando": "espanta", "fecha": "2026-02-16", "contexto": "Estado cognitivo del elector blando en campaña."},
    {"termino": "frustración",      "tipo": "termino", "frecuencia": 209, "funcion_cultural": "emocion", "impacto_voto_blando": "espanta", "fecha": "2026-02-16", "contexto": "Brecha entre expectativas y realidad política."},
    {"termino": "tranquilidad",     "tipo": "termino", "frecuencia": 176, "funcion_cultural": "emocion", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Demanda de calma. Activa voto por estabilidad."},
    {"termino": "calma",            "tipo": "termino", "frecuencia": 132, "funcion_cultural": "emocion", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Valor emocional opuesto a la confrontación."},
    {"termino": "estabilidad",      "tipo": "termino", "frecuencia": 154, "funcion_cultural": "emocion", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Demanda de orden y continuidad. Alta en indecisos."},
    {"termino": "confianza",        "tipo": "termino", "frecuencia": 165, "funcion_cultural": "emocion", "impacto_voto_blando": "activa", "fecha": "2026-02-18", "contexto": "Cuando aparece, activa decisión firme de voto."},
    {"termino": "esperanza",        "tipo": "termino", "frecuencia": 287, "funcion_cultural": "emocion", "impacto_voto_blando": "activa", "fecha": "2026-02-18", "contexto": "Emoción activadora. Opuesta a frustración y miedo."},
    {"termino": "alivio",           "tipo": "termino", "frecuencia": 98,  "funcion_cultural": "emocion", "impacto_voto_blando": "activa", "fecha": "2026-02-18", "contexto": "Sensación post-decisión. Indica voto comprometido."},

    # ── 8. Identidad local moderada ────────────────────────────────────────
    {"termino": "Santa Cruz",       "tipo": "termino", "frecuencia": 387, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-16", "contexto": "Identidad territorial central. Activa orgullo local."},
    {"termino": "cruceño",          "tipo": "termino", "frecuencia": 312, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-16", "contexto": "Identidad étnico-regional. Activador emocional potente."},
    {"termino": "ciudad",           "tipo": "termino", "frecuencia": 218, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-16", "contexto": "Espacio de pertenencia y demanda urbana."},
    {"termino": "familia",          "tipo": "termino", "frecuencia": 254, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Valor central. Activa voto protector y estable."},
    {"termino": "trabajo honesto",  "tipo": "frase",   "frecuencia": 231, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "Ética laboral como identidad cultural cruceña."},
    {"termino": "gente",            "tipo": "termino", "frecuencia": 198, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-17", "contexto": "'La gente quiere...' Narrativa populista suave."},
    {"termino": "esfuerzo",         "tipo": "termino", "frecuencia": 176, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-18", "contexto": "Valor del esfuerzo propio. Activa identificación."},
    {"termino": "respeto",          "tipo": "termino", "frecuencia": 165, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-18", "contexto": "Demanda de respeto ciudadano. Activa voto de dignidad."},
    {"termino": "orden",            "tipo": "termino", "frecuencia": 287, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-19", "contexto": "Valor cultural cruceño. Activa fortemente el voto blando."},
    {"termino": "convivencia",      "tipo": "termino", "frecuencia": 132, "funcion_cultural": "identidad", "impacto_voto_blando": "activa", "fecha": "2026-02-19", "contexto": "Cohesión social. Opuesta a polarización."},
]

def run():
    db = SessionLocal()
    added   = 0
    skipped = 0

    for t in TERMS:
        existing = db.query(LanguageCode).filter(
            LanguageCode.project_id == PID,
            LanguageCode.termino    == t["termino"]
        ).first()
        if existing:
            # Actualizar campos si están vacíos
            changed = False
            if not existing.funcion_cultural and t.get("funcion_cultural"):
                existing.funcion_cultural = t["funcion_cultural"]; changed = True
            if not existing.impacto_voto_blando and t.get("impacto_voto_blando"):
                existing.impacto_voto_blando = t["impacto_voto_blando"]; changed = True
            if changed:
                db.add(existing)
            skipped += 1
            continue

        item = LanguageCode(
            project_id          = PID,
            termino             = t["termino"],
            tipo                = t.get("tipo", "termino"),
            frecuencia          = t.get("frecuencia", 50),
            funcion_cultural    = t.get("funcion_cultural"),
            impacto_voto_blando = t.get("impacto_voto_blando"),
            contexto            = t.get("contexto"),
            fecha_deteccion     = date.fromisoformat(t["fecha"]) if t.get("fecha") else None,
        )
        db.add(item)
        added += 1

    db.commit()
    db.close()
    print(f"✅  {added} términos nuevos agregados, {skipped} ya existían (campos actualizados si faltaban).")

if __name__ == "__main__":
    run()
