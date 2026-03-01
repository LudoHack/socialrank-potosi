"""
Script de datos demo para EtnoDB.
Ejecutar: python seed_demo.py
"""
import os, sys
sys.path.insert(0, '.')

for line in open('.env'):
    if '=' in line and not line.startswith('#'):
        k, v = line.strip().split('=', 1)
        os.environ[k] = v

import models
from database import create_tables, SessionLocal
from datetime import date, timedelta
from models.project import Project
from models.narrative import Narrative
from models.emotion import Emotion
from models.archetype import Archetype
from models.language_code import LanguageCode
from models.community import Community
from models.risk import Risk

create_tables()
db = SessionLocal()

# ── Proyecto ──────────────────────────────────────────────
proyecto = Project(
    nombre="Campaña Municipal 2026",
    cliente="Partido Renovación Ciudadana",
    contexto_pais="Chile",
    fecha_inicio=date(2026, 1, 15),
    descripcion="Investigación etnográfica digital para campaña a alcaldía. Foco en comunas del sur."
)
db.add(proyecto)
db.flush()
pid = proyecto.id

# ── Narrativas ────────────────────────────────────────────
narrativas = [
    ("El sistema político no nos representa", "dominante", "Ciudadanía organizada", date(2026, 1, 20), 9.0),
    ("Necesitamos más seguridad en los barrios", "dominante", "Vecinos Unidos", date(2026, 1, 22), 8.5),
    ("Los jóvenes no tienen futuro en esta ciudad", "emergente", "Movimiento Estudiantil", date(2026, 2, 1), 7.5),
    ("La gestión actual ha fallado en salud", "dominante", "Colectivo de Salud", date(2026, 2, 5), 8.0),
    ("Podemos construir una ciudad más justa", "contrarrelato", "Candidato A", date(2026, 2, 10), 6.5),
    ("La corrupción frena el desarrollo local", "emergente", "Prensa local", date(2026, 2, 14), 7.0),
    ("El empleo local está en crisis", "dominante", "Sindicatos", date(2026, 1, 28), 9.0),
]
for txt, tipo, actor, fecha, peso in narrativas:
    db.add(Narrative(project_id=pid, texto=txt, tipo=tipo,
                     actor_politico=actor, fecha_deteccion=fecha, peso=peso))

# ── Emociones ─────────────────────────────────────────────
emociones = [
    ("ira",           8.2, "Twitter",    date(2026, 1, 15)),
    ("ira",           7.8, "Facebook",   date(2026, 1, 28)),
    ("ira",           8.5, "Twitter",    date(2026, 2, 10)),
    ("miedo",         7.0, "Encuesta",   date(2026, 1, 20)),
    ("miedo",         6.5, "WhatsApp",   date(2026, 2, 5)),
    ("frustracion",   8.8, "Encuesta",   date(2026, 1, 25)),
    ("frustracion",   9.0, "Focus Group",date(2026, 2, 12)),
    ("esperanza",     4.5, "Encuesta",   date(2026, 2, 1)),
    ("esperanza",     5.2, "Eventos",    date(2026, 2, 15)),
    ("desconfianza",  7.5, "Encuesta",   date(2026, 1, 18)),
    ("desconfianza",  8.0, "Twitter",    date(2026, 2, 8)),
    ("orgullo",       3.5, "Focus Group",date(2026, 2, 3)),
    ("orgullo",       4.0, "Encuesta",   date(2026, 2, 18)),
]
for tipo, intens, fuente, fecha in emociones:
    db.add(Emotion(project_id=pid, tipo=tipo, intensidad=intens,
                   fuente=fuente, fecha=fecha))

# ── Arquetipos ────────────────────────────────────────────
arquetipos = [
    ("El trabajador desencantado", "Adulto 35-55 años, empleo informal o precarizado. Votó en el pasado pero perdió la fe en los partidos.", 28.0, "frustracion", ["Radio","WhatsApp","Facebook"], "Estabilidad económica, respeto, trabajo digno", "Desempleo, inseguridad, ser ignorado por la política"),
    ("La madre de familia movilizada", "Mujer 30-50 años, núcleo familiar como eje de su vida. Muy activa en redes sociales de vecinos.", 22.0, "miedo", ["Facebook","WhatsApp","TikTok"], "Seguridad de sus hijos, salud, educación", "Violencia barrial, colapso del sistema de salud"),
    ("El joven frustrado", "18-28 años, educación media o técnica, sin empleo estable. Alto consumo de TikTok e Instagram.", 18.0, "ira", ["TikTok","Instagram","Twitter/X"], "Oportunidades, reconocimiento, futuro", "No poder independizarse, falta de trabajo"),
    ("El vecino organizado", "40-65 años, activo en juntas de vecinos. Pragmático, evalúa gestión concreta.", 15.0, "desconfianza", ["Facebook","Boca a boca","Radio"], "Orden, infraestructura, participación ciudadana", "Promesas incumplidas, corrupción"),
    ("El votante blando", "Perfil moderado, 25-45 años, pendiente de decidir. Se mueve por credibilidad y emoción positiva.", 17.0, "esperanza", ["Instagram","Facebook","TV"], "Soluciones concretas, liderazgo creíble", "Polarización, extremismo, mentiras"),
]
for nombre, desc, peso, emocion, canales, valores, miedos in arquetipos:
    db.add(Archetype(project_id=pid, nombre=nombre, descripcion=desc,
                     peso_relativo=peso, emocion_dominante=emocion,
                     canales=canales, valores_clave=valores, miedos=miedos))

# ── Lenguaje ──────────────────────────────────────────────
lenguaje = [
    ("los de siempre",     "frase",   89, "Referencia a clase política tradicional",          date(2026, 1, 20)),
    ("la gente de verdad", "frase",   67, "Autoidentificación del votante desencantado",       date(2026, 1, 25)),
    ("el abandono",        "frase",   54, "Sensación de olvido por parte del Estado",          date(2026, 2, 1)),
    ("el narco barrio",    "apodo",   43, "Estigma territorial de ciertos sectores",            date(2026, 1, 30)),
    ("los políticos ratas","apodo",  112, "Expresión de rabia popular hacia clase política",   date(2026, 1, 18)),
    ("chao pescao",        "meme",    78, "Expresión de despedida definitiva a candidatos",    date(2026, 2, 8)),
    ("vota nulo es votar", "ironico", 35, "Debate sobre voto nulo en redes",                   date(2026, 2, 12)),
    ("barrio seguro",      "simbolo", 92, "Promesa más valorada por vecinos",                  date(2026, 1, 22)),
    ("manos limpias",      "simbolo", 61, "Demanda de transparencia y anticorrupción",         date(2026, 2, 5)),
    ("con la gente",       "frase",   47, "Slogan de cercanía usado por el candidato A",       date(2026, 2, 10)),
]
for termino, tipo, freq, contexto, fecha in lenguaje:
    db.add(LanguageCode(project_id=pid, termino=termino, tipo=tipo,
                        frecuencia=freq, contexto=contexto, fecha_deteccion=fecha))

# ── Comunidades ───────────────────────────────────────────
comunidades = [
    ("Facebook",    "Vecinos Alerta — Comuna Sur",        "polarizado",    15400, "Grupo muy activo con alto nivel de queja y confrontación. Gran influencia en agenda local.", 9),
    ("WhatsApp",    "Mamás de la Villa Esperanza",        "amplificador",   3200, "Red de madres que amplifica información muy rápidamente. Canal clave para mensajes de salud.", 8),
    ("TikTok",      "Jóvenes x el Cambio",               "activo",         8900, "Creadores de contenido jóvenes. Críticos y creativos, pueden viralizar positivo o negativo.", 7),
    ("Twitter/X",   "Periodistas y opinión pública",     "amplificador",   5600, "Actores de formación de opinión. Bajo volumen, alto impacto en agenda mediática.", 8),
    ("Facebook",    "Padres y Apoderados Movilizados",   "activo",         6700, "Red escolar organizada. Temas: seguridad, educación, drogas en cercanías.", 7),
    ("Radio",       "Audiencia Radio Tierra Sur",        "silencioso",    42000, "Audiencia masiva pero pasiva. Receptiva a mensajes cálidos y cercanos.", 6),
    ("Boca a boca", "Redes de feria y comercio informal","amplificador",  18000, "Transmisión informal de información. Muy efectiva para mensajes simples y concretos.", 7),
]
for plat, nombre, tipo, tam, desc, inf in comunidades:
    db.add(Community(project_id=pid, plataforma=plat, nombre_grupo=nombre,
                     tipo=tipo, tamanio_estimado=tam, descripcion=desc, influencia=inf))

# ── Riesgos ───────────────────────────────────────────────
riesgos = [
    ("Filtración de audios comprometedores del candidato aliado", "Circulan audios en WhatsApp con declaraciones polémicas de un aliado del partido. Alta probabilidad de viralización.", "rojo", 5, date(2026, 2, 20)),
    ("Campaña de desinformación sobre gestión de fondos",         "Cuentas anónimas difunden acusaciones de malversación sin evidencia verificada. Crecimiento rápido.", "rojo", 4, date(2026, 2, 18)),
    ("Aumento de percepción de inseguridad post-incidentes",      "Tres robos violentos en sector céntrico generaron pánico en redes. El tema domina la conversación.", "amarillo", 4, date(2026, 2, 15)),
    ("Baja adhesión de votantes jóvenes en encuestas",            "Los menores de 30 años muestran alta intención de voto nulo o abstención según últimas encuestas.", "amarillo", 3, date(2026, 2, 10)),
    ("Competidor lanza propuesta de empleo local potente",        "Candidato opositor anunció plan de empleo con datos concretos. Buena recepción en medios.", "amarillo", 3, date(2026, 2, 19)),
    ("Tensión interna en comando de campaña",                     "Diferencias estratégicas internas según fuentes. Controlado por ahora.", "verde", 2, date(2026, 2, 12)),
]
for tema, desc, nivel, vel, fecha in riesgos:
    db.add(Risk(project_id=pid, tema=tema, descripcion=desc,
                nivel=nivel, velocidad_crecimiento=vel,
                fecha_deteccion=fecha, activo=True))

db.commit()
db.close()
print("Demo cargado exitosamente.")
print(f"  Proyecto ID: {pid}")
print(f"  Narrativas:  {len(narrativas)}")
print(f"  Emociones:   {len(emociones)}")
print(f"  Arquetipos:  {len(arquetipos)}")
print(f"  Lenguaje:    {len(lenguaje)}")
print(f"  Comunidades: {len(comunidades)}")
print(f"  Riesgos:     {len(riesgos)}")
print()
print("Abre http://localhost:5173 y activa el proyecto 'Campana Municipal 2026'")
