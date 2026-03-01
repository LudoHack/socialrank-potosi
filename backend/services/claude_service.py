"""
Servicio de IA usando Google Gemini Flash (GRATIS).
Modelo: gemini-2.5-flash
API key gratuita en: https://aistudio.google.com/apikey
"""
import json
from google import genai
from google.genai import types
from config import settings


def _call_gemini(prompt: str) -> dict:
    if not settings.gemini_api_key:
        return {"error": "GEMINI_API_KEY no configurada. Configúrala en las variables de entorno del servicio."}
    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        resp = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.4,
                response_mime_type="application/json",
            ),
        )
        raw = resp.text.strip()
        # Limpiar posibles bloques de codigo markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.rsplit("```", 1)[0]
        try:
            return json.loads(raw)
        except Exception as e:
            return {"error": f"No se pudo parsear la respuesta: {e}", "raw": raw}
    except Exception as e:
        return {"error": f"Error al llamar a la IA: {str(e)}"}


def simulate_message(mensaje: str, context: dict) -> dict:
    arquetipos_txt = "\n".join([
        f"- {a['nombre']} ({a['peso']}% del publico): emocion dominante={a['emocion']}, "
        f"valores={a['valores']}, miedos={a['miedos']}, canales={a['canales']}"
        for a in context.get("arquetipos", [])
    ]) or "Sin arquetipos definidos."

    emociones_txt = ", ".join([
        f"{e['tipo']}={e['intensidad']}/10"
        for e in context.get("emociones", [])[:10]
    ]) or "Sin datos emocionales."

    narrativas_txt = "\n".join([
        f"- [{n['tipo']}] {n['texto']} (peso={n['peso']})"
        for n in context.get("narrativas_top", [])
    ]) or "Sin narrativas registradas."

    riesgos_txt = "\n".join([
        f"- RIESGO CRITICO: {r['tema']}"
        for r in context.get("riesgos_criticos", [])
    ]) or "Sin riesgos criticos activos."

    prompt = f"""Eres un experto en comunicacion politica y etnografia digital.
Analiza el siguiente mensaje en el contexto del proyecto "{context['proyecto']}" ({context.get('contexto_pais','')}).

MENSAJE A SIMULAR:
"{mensaje}"

ARQUETIPOS DEL PUBLICO:
{arquetipos_txt}

ESTADO EMOCIONAL ACTUAL:
{emociones_txt}

NARRATIVAS DOMINANTES:
{narrativas_txt}

{riesgos_txt}

Responde UNICAMENTE con este JSON (sin texto adicional):
{{
  "resumen_ejecutivo": "Parrafo breve de evaluacion general del mensaje",
  "riesgo_general": "bajo|medio|alto|critico",
  "reacciones_por_arquetipo": [
    {{
      "arquetipo": "nombre del arquetipo",
      "reaccion_esperada": "descripcion de como reaccionaria",
      "emocion_activada": "emocion principal que activa",
      "nivel_receptividad": "alto|medio|bajo|rechazo"
    }}
  ],
  "fortalezas_del_mensaje": ["punto fuerte 1", "punto fuerte 2"],
  "riesgos_del_mensaje": ["riesgo 1", "riesgo 2"],
  "ajuste_de_tono_sugerido": "Sugerencia concreta para mejorar el mensaje",
  "version_optimizada": "Version mejorada del mensaje (max 2 oraciones)"
}}"""

    return _call_gemini(prompt)


def generate_recommendations(context: dict) -> dict:
    arquetipos_txt = "\n".join([
        f"- {a['nombre']} ({a['peso']}%): emocion={a['emocion']}, canales={a['canales']}"
        for a in context.get("arquetipos", [])
    ]) or "Sin arquetipos."

    narrativas_txt = "\n".join([
        f"- [{n['tipo']}] {n['texto']}"
        for n in context.get("narrativas_top", [])
    ]) or "Sin narrativas."

    emociones_txt = ", ".join([
        f"{e['tipo']}={e['intensidad']}/10"
        for e in context.get("emociones", [])[:8]
    ]) or "Sin datos."

    riesgos_txt = "\n".join([
        f"- [{r['nivel'].upper()}] {r['tema']}"
        for r in context.get("riesgos_criticos", [])
    ]) or "Sin riesgos criticos."

    prompt = f"""Eres un estratega de comunicacion politica y etnografia digital.
Genera recomendaciones estrategicas para el proyecto "{context['proyecto']}" en {context.get('contexto_pais','')}.

ARQUETIPOS:
{arquetipos_txt}

NARRATIVAS DOMINANTES:
{narrativas_txt}

ESTADO EMOCIONAL:
{emociones_txt}

RIESGOS ACTIVOS:
{riesgos_txt}

Responde UNICAMENTE con este JSON (sin texto adicional):
{{
  "diagnostico_general": "Diagnostico de 2-3 oraciones del estado actual",
  "que_decir": [
    {{"mensaje": "...", "razon": "...", "arquetipo_objetivo": "..."}}
  ],
  "que_no_decir": [
    {{"mensaje": "...", "razon": "..."}}
  ],
  "canales_prioritarios": [
    {{"canal": "...", "razon": "...", "formato_recomendado": "..."}}
  ],
  "tono_recomendado": {{
    "descripcion": "...",
    "palabras_clave": ["...", "..."],
    "palabras_a_evitar": ["...", "..."]
  }},
  "momento_optimo": {{
    "descripcion": "...",
    "urgencia": "inmediata|esta_semana|este_mes"
  }},
  "acciones_prioritarias": [
    {{"accion": "...", "prioridad": "alta|media|baja", "plazo": "..."}}
  ]
}}"""

    return _call_gemini(prompt)
