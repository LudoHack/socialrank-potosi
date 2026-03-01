"""
Seed de datos para Gobernación del Departamento de Santa Cruz de la Sierra — Bolivia
Ejecutar: python seed_gobernacion.py
"""
import os, sys
sys.path.insert(0, '.')

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

# Limpiar datos previos
for M in [Risk, Community, LanguageCode, Archetype, Emotion, Narrative, Project]:
    db.query(M).delete()
db.commit()

# ── Proyecto ──────────────────────────────────────────────────────────────
proyecto = Project(
    nombre="Elecciones Gobernación Dpto. Santa Cruz de la Sierra",
    cliente="Social Rank Bolivia",
    contexto_pais="Bolivia",
    fecha_inicio=date(2026, 1, 10),
    descripcion="Análisis etnográfico digital para la campaña a la Gobernación del Departamento de Santa Cruz. Foco en identidad regional, gestión departamental y voto blando cruceño."
)
db.add(proyecto)
db.flush()
pid = proyecto.id

# ── Narrativas ────────────────────────────────────────────────────────────
narrativas = [
    ("La gobernación abandona al campo y los municipios del interior", "dominante",
     "Comunidades rurales y alcaldes del interior", date(2026, 1, 15), 9.2),
    ("Los recursos del gas y la agroindustria no benefician a todos los cruceños", "dominante",
     "Organizaciones campesinas y sectores populares", date(2026, 1, 20), 8.8),
    ("Las carreteras departamentales están destruidas y sin mantenimiento", "dominante",
     "Transportistas, productores y cívicos", date(2026, 1, 22), 8.5),
    ("El gobernador prioriza la política nacional sobre la gestión local", "emergente",
     "Prensa y analistas políticos", date(2026, 2, 1), 7.8),
    ("Santa Cruz puede ser un departamento modelo con autonomía real", "contrarrelato",
     "Candidatos y movimiento autonomista", date(2026, 2, 5), 7.2),
    ("La salud pública departamental está en colapso en el interior", "dominante",
     "Organizaciones de salud y comunidades", date(2026, 2, 8), 8.3),
    ("La identidad camba y la autonomía son valores no negociables", "dominante",
     "Comité Cívico Pro Santa Cruz", date(2026, 1, 28), 8.0),
    ("Los jóvenes cruceños no tienen futuro si no hay inversión departamental", "emergente",
     "Movimiento estudiantil y juventudes", date(2026, 2, 12), 7.5),
]
for txt, tipo, actor, fecha, peso in narrativas:
    db.add(Narrative(project_id=pid, texto=txt, tipo=tipo,
                     actor_politico=actor, fecha_deteccion=fecha, peso=peso))

# ── Emociones ─────────────────────────────────────────────────────────────
# Fuentes: escucha social y bigdata (sin encuestas ni focus groups)
emociones = [
    # IRA — semana 1 (10–16 ene)
    ("ira",          8.6, "Twitter/X",         date(2026, 1, 11), "Pico de indignación por anuncio de alza de tarifas de servicios departamentales"),
    ("ira",          7.9, "Facebook",           date(2026, 1, 12), "Comentarios virales contra gestión de obras inconclusas en Santa Cruz"),
    ("ira",          8.3, "TikTok",             date(2026, 1, 14), "Videos de baches y calles inundadas con alta difusión"),
    # IRA — semana 2 (17–23 ene)
    ("ira",          8.1, "Telegram",           date(2026, 1, 18), "Grupos políticos difunden denuncias sobre contratos irregulares"),
    ("ira",          8.7, "Twitter/X",          date(2026, 1, 22), "Trending #GobernacionResponde por corte de agua en zonas rurales"),
    # IRA — semana 3-4 (24 ene – 10 feb)
    ("ira",          7.5, "Facebook",           date(2026, 1, 29), "Compartidos masivos de notas sobre licitación cuestionada"),
    ("ira",          8.9, "Twitter/X",          date(2026, 2, 8),  "Reacción a declaraciones del gobernador sobre el agro"),
    ("ira",          9.1, "Instagram",          date(2026, 2, 11), "Reels de protestas en carreteras departamentales"),

    # MIEDO — escucha social
    ("miedo",        7.2, "Twitter/X",          date(2026, 1, 13), "Temor al centralismo tras declaraciones del gobierno nacional"),
    ("miedo",        6.8, "WhatsApp viral",     date(2026, 1, 21), "Cadenas sobre posible intervención federal a tierras productivas"),
    ("miedo",        7.5, "Facebook",           date(2026, 1, 27), "Comentarios sobre crisis de diésel y su impacto en cosecha"),
    ("miedo",        7.0, "Telegram",           date(2026, 2, 3),  "Difusión de audios sobre deuda departamental no comunicada"),
    ("miedo",        6.5, "TikTok",             date(2026, 2, 9),  "Contenido viral sobre pérdida de autonomía departamental"),
    ("miedo",        7.8, "Twitter/X",          date(2026, 2, 14), "Reacción a proyecto de ley que afecta gestión de recursos hídricos"),

    # FRUSTRACION — bigdata social
    ("frustracion",  8.7, "Twitter/X",          date(2026, 1, 15), "Saturación de quejas sobre falta de mantenimiento vial"),
    ("frustracion",  8.4, "Facebook",           date(2026, 1, 23), "Grupos de vecinos comparten fotos de infraestructura deteriorada"),
    ("frustracion",  9.1, "Instagram",          date(2026, 2, 1),  "Historias y reels sobre promesas incumplidas de candidatos"),
    ("frustracion",  8.8, "Twitter/X",          date(2026, 2, 7),  "Hashtag #NosCansamosDeEsperar con miles de impresiones"),
    ("frustracion",  9.3, "TikTok",             date(2026, 2, 13), "Videos virales comparando gestión anterior vs actual"),
    ("frustracion",  8.6, "YouTube",            date(2026, 2, 19), "Comentarios en notas de medios locales sobre obras sin terminar"),

    # ESPERANZA — señales débiles
    ("esperanza",    4.8, "Facebook",           date(2026, 1, 17), "Reacciones positivas a propuesta de candidato independiente"),
    ("esperanza",    5.2, "Twitter/X",          date(2026, 1, 26), "Respaldo a agenda de transparencia presentada en foro"),
    ("esperanza",    5.5, "Instagram",          date(2026, 2, 4),  "Cobertura positiva de acto comunitario en municipios del interior"),
    ("esperanza",    6.1, "YouTube",            date(2026, 2, 10), "Video de propuesta productiva con amplia recepción orgánica"),
    ("esperanza",    5.8, "Facebook",           date(2026, 2, 16), "Movilización de jóvenes cruceños en torno a plataforma cívica"),
    ("esperanza",    6.3, "TikTok",             date(2026, 2, 20), "Contenido positivo sobre potencial agropecuario del departamento"),

    # DESCONFIANZA — señal dominante
    ("desconfianza", 7.8, "Twitter/X",          date(2026, 1, 16), "Escepticismo ante cifras oficiales de inversión departamental"),
    ("desconfianza", 8.2, "Facebook",           date(2026, 1, 24), "Comentarios desconfiados ante actos de campaña anticipada"),
    ("desconfianza", 8.5, "Telegram",           date(2026, 1, 30), "Difusión de análisis ciudadano que cuestiona rendición de cuentas"),
    ("desconfianza", 8.0, "Twitter/X",          date(2026, 2, 6),  "Reacción viral a nota de investigación periodística"),
    ("desconfianza", 8.7, "Instagram",          date(2026, 2, 12), "Infografías virales sobre inconsistencias en el presupuesto"),
    ("desconfianza", 9.0, "YouTube",            date(2026, 2, 18), "Comentarios a entrevista donde candidato evita responder"),

    # ORGULLO — identidad camba
    ("orgullo",      6.5, "Instagram",          date(2026, 1, 20), "Contenido sobre identidad regional camba con alta interacción"),
    ("orgullo",      7.2, "TikTok",             date(2026, 1, 31), "Videos de fiestas y tradiciones cruceñas con millones de vistas"),
    ("orgullo",      6.8, "Facebook",           date(2026, 2, 5),  "Comunidades de cruceños en exterior compartiendo contenido regional"),
    ("orgullo",      7.0, "Twitter/X",          date(2026, 2, 15), "Debate sobre autonomía departamental activa sentimiento identitario"),
    ("orgullo",      7.5, "YouTube",            date(2026, 2, 21), "Documental sobre productores agropecuarios con alta difusión orgánica"),
]
for tipo, intens, fuente, fecha, notas in emociones:
    db.add(Emotion(project_id=pid, tipo=tipo, intensidad=intens,
                   fuente=fuente, fecha=fecha, notas=notas))

# ── Arquetipos ────────────────────────────────────────────────────────────
arquetipos = [
    ("El productor agropecuario desencantado",
     "Hombre 40-65 años, productor soyero, ganadero o agricultor del interior. Votó por el autonomismo pero siente que la gestión departamental lo ignora. Muy influyente en su comunidad.",
     26.0, "frustracion",
     ["WhatsApp", "Radio FM", "Facebook"],
     "Infraestructura vial, mercados, crédito agrícola, autonomía",
     "Centralismo de La Paz, pérdida de tierras, burocracia departamental"),
    ("El cívico desencantado",
     "Hombre o mujer 35-60 años, Santa Cruz ciudad. Identidad camba fuerte. Apoyó la autonomía pero siente que los líderes la traicionaron por ambiciones personales.",
     22.0, "desconfianza",
     ["Facebook", "Twitter/X", "Boca a boca"],
     "Autonomía real, transparencia, gestión eficiente, identidad regional",
     "Corrupción, politización del Comité Cívico, pérdida de valores autonomistas"),
    ("La mujer del municipio del interior",
     "Mujer 28-50 años de provincias como Ñuflo de Chávez, Velasco o Warnes. Muy activa en redes locales. El acceso a salud y educación es su prioridad absoluta.",
     20.0, "miedo",
     ["WhatsApp", "Facebook", "Radio comunitaria"],
     "Hospital equipado, escuelas con maestros, agua potable, seguridad",
     "Olvido del interior, servicios inexistentes, tener que viajar a SCZ para atención"),
    ("El joven camba urbano",
     "18-30 años, Santa Cruz ciudad o municipios medianos. Alta identidad regional pero frustrado con la falta de oportunidades. Alto consumo de TikTok e Instagram.",
     18.0, "ira",
     ["TikTok", "Instagram", "Twitter/X"],
     "Empleo, innovación, identidad cruceña, futuro en Santa Cruz",
     "Migración forzada, políticos de siempre, falta de meritocracia"),
    ("El votante blando departamental",
     "Perfil mixto, 25-50 años. No tiene identidad política fija. Evalúa candidatos por propuestas concretas de infraestructura, salud y economía. Define elecciones.",
     14.0, "esperanza",
     ["Facebook", "WhatsApp", "TV local"],
     "Soluciones concretas, obras visibles, liderazgo creíble",
     "Polarización, promesas vacías, gestión centralista"),
]
for nombre, desc, peso, emocion, canales, valores, miedos in arquetipos:
    db.add(Archetype(project_id=pid, nombre=nombre, descripcion=desc,
                     peso_relativo=peso, emocion_dominante=emocion,
                     canales=canales, valores_clave=valores, miedos=miedos))

# ── Lenguaje (80 términos, 8 categorías) ─────────────────────────────────
FUNC = {
    "indecision":   "indecision",
    "desconfianza": "desconfianza",
    "activacion":   "activacion",
    "espanto":      "espanto",
    "economia":     "economia",
    "gestion":      "gestion",
    "emocion":      "emocion",
    "identidad":    "identidad",
}

lenguaje_data = [
    # IDENTIDAD LOCAL (12)
    ("camba",               "frase",   134, "identidad", "alto",    "Identidad regional cruceña, orgullo de ser del oriente boliviano",         date(2026, 1, 15)),
    ("tierra camba",        "simbolo", 112, "identidad", "alto",    "Referencia al territorio y herencia cultural cruceña",                     date(2026, 1, 18)),
    ("autonomía ya",        "frase",   128, "identidad", "alto",    "Demanda de autonomía departamental real y efectiva",                        date(2026, 1, 20)),
    ("oriente boliviano",   "frase",    89, "identidad", "medio",   "Autoidentificación del bloque oriental frente al occidente",               date(2026, 1, 22)),
    ("nación camba",        "simbolo",  76, "identidad", "medio",   "Movimiento de identidad regional con tono separatista moderado",           date(2026, 1, 25)),
    ("cruceño de corazón",  "frase",    94, "identidad", "alto",    "Expresión de arraigo e identidad usada en campaña",                        date(2026, 2, 1)),
    ("el oriente produce",  "frase",    83, "identidad", "medio",   "Argumento económico de la región frente al centralismo",                   date(2026, 2, 3)),
    ("la media luna",       "simbolo",  71, "identidad", "medio",   "Referencia histórica al bloque autonomista de cuatro departamentos",       date(2026, 2, 5)),
    ("la llajta cruceña",   "frase",    67, "identidad", "medio",   "Término afectivo para referirse a Santa Cruz ciudad",                      date(2026, 2, 8)),
    ("ser del interior",    "frase",    58, "identidad", "bajo",    "Autoidentificación de municipios del interior del departamento",           date(2026, 2, 10)),
    ("el departamento vive","frase",    52, "identidad", "medio",   "Slogan de campaña sobre el potencial departamental",                       date(2026, 2, 12)),
    ("sangre camba",        "frase",    44, "identidad", "bajo",    "Expresión extrema de identidad regional usada en redes",                   date(2026, 2, 15)),

    # ECONOMÍA COTIDIANA (12)
    ("los del campo",       "frase",    97, "economia", "alto",    "Referencia a productores rurales como base económica del departamento",    date(2026, 1, 15)),
    ("las carreteras rotas","frase",   118, "economia", "alto",    "Demanda principal de productores y transportistas del interior",           date(2026, 1, 18)),
    ("el agro primero",     "frase",    86, "economia", "alto",    "Prioridad del sector agropecuario en el debate político",                  date(2026, 1, 22)),
    ("sin caminos no hay cosecha", "frase", 109, "economia", "alto","Relación directa entre infraestructura y producción",                    date(2026, 1, 26)),
    ("la soya nos da de comer", "frase", 78, "economia", "medio",  "Defensa del modelo agroindustrial soyero ante críticas ambientales",      date(2026, 2, 1)),
    ("el mercado chino",    "frase",    65, "economia", "medio",   "Referencia a exportaciones al mercado asiático como oportunidad",         date(2026, 2, 4)),
    ("el precio del diesel","frase",    92, "economia", "alto",    "Crisis de abastecimiento de combustible que afecta al agro",              date(2026, 2, 8)),
    ("las regalías son nuestras","frase",103,"economia","alto",    "Demanda de mayor retención de regalías hidrocarburíferas en el dpto.",    date(2026, 2, 10)),
    ("economía regional",   "frase",    71, "economia", "medio",   "Concepto de desarrollo endógeno departamental",                           date(2026, 2, 12)),
    ("el dólar sube",       "frase",    84, "economia", "alto",    "Crisis cambiaria que golpea a productores e importadores",                date(2026, 2, 15)),
    ("falta inversión",     "frase",    89, "economia", "alto",    "Crítica a la baja inversión departamental en infraestructura",            date(2026, 2, 18)),
    ("el campo sufre",      "frase",    76, "economia", "medio",   "Expresión de angustia del sector rural ante la crisis",                   date(2026, 2, 20)),

    # GESTIÓN (10)
    ("obras prometidas",    "frase",   103, "gestion", "alto",    "Referencia irónica a promesas de campaña no cumplidas",                   date(2026, 1, 16)),
    ("el gobernador no está","frase",   95, "gestion", "alto",    "Crítica a la ausencia o distracción del gobernador en gestión local",     date(2026, 1, 20)),
    ("licitaciones turbias", "frase",   88, "gestion", "alto",    "Denuncias de corrupción en contratos de obras departamentales",           date(2026, 1, 25)),
    ("sin rendición de cuentas","frase",79, "gestion", "medio",   "Falta de transparencia en el manejo de fondos departamentales",           date(2026, 2, 1)),
    ("los hospitales vacíos","frase",   107, "gestion", "alto",   "Crítica al sistema de salud pública departamental sin insumos",           date(2026, 2, 5)),
    ("el ejecutivo departamental","frase",63,"gestion","bajo",    "Referencia técnica a la estructura del gobierno departamental",           date(2026, 2, 8)),
    ("asamblea bloqueada",  "frase",    71, "gestion", "medio",   "Conflictos políticos que paralizan la Asamblea Legislativa Departamental",date(2026, 2, 10)),
    ("plan de desarrollo",  "frase",    58, "gestion", "bajo",    "Demanda de planificación estratégica departamental de largo plazo",       date(2026, 2, 12)),
    ("los técnicos del dpto","frase",   44, "gestion", "bajo",    "Referencia al aparato burocrático departamental",                        date(2026, 2, 15)),
    ("gestión transparente","frase",    82, "gestion", "medio",   "Demanda ciudadana de transparencia en el manejo público",                 date(2026, 2, 18)),

    # INDECISIÓN (10)
    ("no sé a quién votar", "frase",    98, "indecision", "alto",  "Expresión masiva de indecisión ante opciones electorales poco claras",   date(2026, 1, 18)),
    ("todos son iguales",   "frase",   112, "indecision", "alto",  "Percepción de falta de diferencia entre candidatos",                     date(2026, 1, 22)),
    ("ver para creer",      "frase",    87, "indecision", "medio", "Demanda de propuestas concretas antes de comprometerse",                  date(2026, 1, 28)),
    ("esperar y ver",       "frase",    74, "indecision", "medio", "Actitud pasiva ante el proceso electoral",                               date(2026, 2, 3)),
    ("no me convence ninguno","frase",  91, "indecision", "alto",  "Rechazo a todos los candidatos por parte del votante blando",            date(2026, 2, 7)),
    ("quizás vote nulo",    "frase",    68, "indecision", "medio", "Amenaza de voto nulo como señal de descontento",                         date(2026, 2, 10)),
    ("lo pienso más",       "frase",    55, "indecision", "bajo",  "Expresión de indecisión detectada en escucha social y análisis digital",                    date(2026, 2, 13)),
    ("no hay candidato bueno","frase",  83, "indecision", "alto",  "Percepción de ausencia de opciones positivas",                           date(2026, 2, 16)),
    ("el que menos roba",   "meme",     77, "indecision", "medio", "Humor negro que refleja la desconfianza generalizada",                   date(2026, 2, 18)),
    ("ni uno ni otro",      "frase",    62, "indecision", "medio", "Posición ambivalente ante polarización política departamental",          date(2026, 2, 20)),

    # DESCONFIANZA (10)
    ("los políticos mienten","frase",  124, "desconfianza", "alto",  "Afirmación generalizada de desconfianza en clase política",            date(2026, 1, 15)),
    ("esto es un negocio",  "frase",   108, "desconfianza", "alto",  "Percepción de que la política departamental sirve intereses privados", date(2026, 1, 20)),
    ("la trampa electoral", "frase",    89, "desconfianza", "alto",  "Desconfianza en el proceso y resultados electorales",                  date(2026, 1, 25)),
    ("vienen cada 5 años",  "frase",    96, "desconfianza", "alto",  "Crítica al oportunismo electoral de los candidatos",                   date(2026, 1, 30)),
    ("me prometieron y nada","frase",   87, "desconfianza", "alto", "Experiencia personal de promesas incumplidas de gestiones anteriores",  date(2026, 2, 4)),
    ("el comité ya no sirve","frase",   73, "desconfianza", "medio","Pérdida de credibilidad del Comité Cívico Pro Santa Cruz",              date(2026, 2, 8)),
    ("están coludidos",     "frase",    81, "desconfianza", "alto", "Percepción de acuerdos oscuros entre candidatos o partidos",            date(2026, 2, 11)),
    ("las encuestas mienten","frase",   66, "desconfianza", "medio","Desconfianza en sondeos y encuestas de intención de voto",              date(2026, 2, 14)),
    ("nadie rinde cuentas", "frase",    78, "desconfianza", "alto", "Falta de accountability en la gestión departamental",                   date(2026, 2, 17)),
    ("todo es teatro",      "meme",     59, "desconfianza", "medio","Percepción de que los debates y actos políticos son mera actuación",    date(2026, 2, 20)),

    # ACTIVACIÓN (8)
    ("hay que votar igual", "frase",    92, "activacion", "alto",   "Llamado a la participación electoral pese al descontento",              date(2026, 1, 16)),
    ("el cambio viene del voto","frase",107, "activacion", "alto",  "Argumento de la importancia del voto como herramienta de cambio",      date(2026, 1, 22)),
    ("juntémonos a decidir","frase",    78, "activacion", "medio",  "Llamado a la organización comunitaria para decidir el voto",            date(2026, 1, 28)),
    ("ya basta de lo mismo","frase",    115, "activacion", "alto",  "Slogan de ruptura con el status quo departamental",                     date(2026, 2, 2)),
    ("el pueblo elige",     "frase",    88, "activacion", "alto",   "Afirmación de soberanía popular en el proceso electoral",               date(2026, 2, 6)),
    ("actívate Santa Cruz", "frase",    71, "activacion", "medio",  "Llamado a la movilización ciudadana cruceña",                           date(2026, 2, 10)),
    ("organízate o te organizan","meme",63, "activacion", "medio",  "Advertencia irónica sobre participación o pasividad",                  date(2026, 2, 14)),
    ("este voto sí importa","frase",    84, "activacion", "alto",   "Mensaje de alta relevancia del voto departamental",                     date(2026, 2, 18)),

    # ESPANTO (9)
    ("el centralismo nos aplasta","frase",118,"espanto","alto",    "Miedo al control del gobierno nacional sobre el departamento",           date(2026, 1, 15)),
    ("nos van a quitar las tierras","frase",103,"espanto","alto",  "Temor a la reversión de dotaciones de tierra en el oriente",            date(2026, 1, 19)),
    ("nos quedamos sin gas","frase",    97, "espanto", "alto",     "Miedo al agotamiento o centralización de los recursos hidrocarburíferos",date(2026, 1, 23)),
    ("el país se rompe",    "frase",    88, "espanto", "alto",     "Miedo a una crisis de gobernabilidad o fractura política nacional",     date(2026, 1, 27)),
    ("nos invaden",         "frase",    74, "espanto", "medio",    "Expresión xenófoba o defensiva ante migración interna al dpto.",        date(2026, 2, 1)),
    ("la próxima crisis",   "frase",    81, "espanto", "alto",     "Temor a una nueva crisis económica como la de 2019-2020",              date(2026, 2, 6)),
    ("sin autonomía no hay futuro","frase",92,"espanto","alto",    "Miedo a perder los avances autonómicos conseguidos",                    date(2026, 2, 10)),
    ("el dpto. endeudado",  "frase",    69, "espanto", "medio",    "Preocupación por la deuda departamental y su impacto en obras",        date(2026, 2, 15)),
    ("nos van a dejar solos","frase",   58, "espanto", "bajo",     "Miedo al abandono del gobierno central ante una crisis local",         date(2026, 2, 19)),

    # EMOCIONAL BLANDO (9)
    ("Santa Cruz es mi orgullo","frase",104,"emocion","alto",      "Expresión de amor y orgullo por el departamento",                       date(2026, 1, 16)),
    ("por mis hijos voto",  "frase",    95, "emocion", "alto",     "Motivación familiar como impulso principal del voto",                   date(2026, 1, 21)),
    ("quiero ver prosperar el campo","frase",82,"emocion","alto",  "Aspiración emocional del sector rural hacia el bienestar",             date(2026, 1, 26)),
    ("me cansa la política","frase",    88, "emocion", "alto",     "Fatiga política y emocional muy extendida en el electorado",            date(2026, 2, 1)),
    ("cuándo cambia esto",  "frase",    76, "emocion", "medio",    "Angustia ante la percepción de estancamiento departamental",            date(2026, 2, 5)),
    ("sueño con un SCZ diferente","frase",67,"emocion","medio",    "Aspiración de cambio positivo expresada emocionalmente",               date(2026, 2, 9)),
    ("la gente de bien",    "frase",    71, "emocion", "medio",    "Autoidentificación del votante moderado como ciudadano decente",        date(2026, 2, 13)),
    ("cansado pero voto",   "frase",    59, "emocion", "bajo",     "Actitud de resignación activa muy común en el electorado",              date(2026, 2, 17)),
    ("confío en el cambio", "frase",    63, "emocion", "bajo",     "Esperanza cautelosa depositada en candidatos de renovación",           date(2026, 2, 20)),
]

for termino, tipo, freq, func, impacto, contexto, fecha in lenguaje_data:
    db.add(LanguageCode(
        project_id=pid, termino=termino, tipo=tipo,
        frecuencia=freq, funcion_cultural=func,
        impacto_voto_blando=impacto, contexto=contexto,
        fecha_deteccion=fecha
    ))

# ── Comunidades ───────────────────────────────────────────────────────────
comunidades = [
    ("Facebook",    "Cruceños Organizados — Departamento SCZ",  "polarizado",    38000,
     "Grupo de alto volumen y polarización. Narrativas autonomistas y crítica al gobierno central y departamental. Gran influencia en la agenda local.", 9),
    ("WhatsApp",    "Productores del Norte Integrado",           "amplificador",   8500,
     "Red de productores soyeros y ganaderos. Amplifica información sobre precios, insumos y política agraria. Canal clave para el voto rural.", 9),
    ("TikTok",      "Jóvenes Cambas SCZ",                        "activo",        24000,
     "Creadores de contenido con fuerte identidad regional. Críticos, creativos y con alto poder de viralización positivo o negativo.", 8),
    ("Twitter/X",   "Cívicos y Periodistas Santa Cruz",          "amplificador",  12000,
     "Formadores de opinión con alto impacto en agenda mediática. Bajo volumen pero muy influyentes en el debate político departamental.", 8),
    ("Facebook",    "Mujeres del Interior — Provincias SCZ",     "activo",        15000,
     "Red de mujeres de municipios del interior. Temas: salud, educación, agua potable. Muy activas en épocas electorales.", 7),
    ("Radio",       "Audiencia Radios FM de Santa Cruz",         "silencioso",   180000,
     "Audiencia masiva y pasiva. Altamente receptiva a mensajes emotivos e identitarios. El formato radial sigue siendo dominante en el interior.", 7),
    ("Boca a boca", "Redes de ferias y mercados departamentales","amplificador",  55000,
     "Transmisión informal muy efectiva en comunidades rurales. Mensajes simples y concretos tienen alta penetración en este canal.", 8),
]
for plat, nombre, tipo, tam, desc, inf in comunidades:
    db.add(Community(project_id=pid, plataforma=plat, nombre_grupo=nombre,
                     tipo=tipo, tamanio_estimado=tam, descripcion=desc, influencia=inf))

# ── Riesgos ───────────────────────────────────────────────────────────────
riesgos = [
    ("Escándalo de corrupción en licitación de carretera departamental",
     "Documentos filtrados revelan sobreprecio del 40% en contrato de construcción vial. WhatsApp y Facebook en ebullición. Alto potencial de daño electoral.",
     "rojo", 5, date(2026, 2, 18)),
    ("Crisis de abastecimiento de diésel afecta cosecha",
     "Escasez de combustible en el norte integrado amenaza la cosecha de soya. El sector agropecuario culpa directamente al gobierno departamental por inacción.",
     "rojo", 5, date(2026, 2, 15)),
    ("Candidato opositor lanza propuesta de salud rural potente",
     "Competidor presenta plan concreto de hospitales en municipios del interior con financiamiento definido. Buena recepción en medios y redes del interior.",
     "amarillo", 4, date(2026, 2, 19)),
    ("Tensión entre Comité Cívico y candidatura oficialista",
     "Ruptura visible entre el Comité Pro Santa Cruz y el candidato del movimiento en el poder. Puede fragmentar el voto autonomista.",
     "amarillo", 4, date(2026, 2, 12)),
    ("Baja participación esperada en municipios del interior",
     "Encuestas revelan alta intención de abstención en 8 provincias del interior por descontento con todas las opciones.",
     "amarillo", 3, date(2026, 2, 10)),
    ("Campaña de desinformación sobre origen de candidato",
     "Cuentas anónimas cuestionan la identidad regional del candidato principal. Narrativa en crecimiento en redes sociales.",
     "verde", 2, date(2026, 2, 20)),
]
for tema, desc, nivel, vel, fecha in riesgos:
    db.add(Risk(project_id=pid, tema=tema, descripcion=desc,
                nivel=nivel, velocidad_crecimiento=vel,
                fecha_deteccion=fecha, activo=True))

db.commit()
db.close()

print("Gobernacion cargada exitosamente.")
print(f"  Proyecto ID:   {pid}")
print(f"  Narrativas:    {len(narrativas)}")
print(f"  Emociones:     {len(emociones)}")
print(f"  Arquetipos:    {len(arquetipos)}")
print(f"  Lenguaje:      {len(lenguaje_data)} terminos")
print(f"  Comunidades:   {len(comunidades)}")
print(f"  Riesgos:       {len(riesgos)}")
