"""
Seed de datos — Gobierno del Estado Plurinacional de Bolivia 2026
Monitoreo de percepción ciudadana, narrativas dominantes y riesgos políticos
Ejecutar: python seed_gobierno.py
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
    nombre="Monitoreo Gobierno Nacional Bolivia 2026",
    cliente="Social Rank Bolivia — Presidencia",
    contexto_pais="Bolivia",
    fecha_inicio=date(2026, 1, 1),
    descripcion="Análisis etnográfico digital del Gobierno del Estado Plurinacional de Bolivia. Monitoreo de percepción ciudadana, narrativas dominantes, riesgos políticos y mapa emocional nacional para la toma de decisiones estratégicas del Poder Ejecutivo."
)
db.add(proyecto)
db.flush()
pid = proyecto.id

# ── Narrativas ────────────────────────────────────────────────────────────
narrativas = [
    ("La caída en la producción de gas reduce los ingresos del Estado y presiona el presupuesto de inversión pública", "dominante",
     "Economistas, empresarios y analistas del sector energético", date(2026, 1, 8), 8.9),
    ("La escasez de combustible paraliza Bolivia y el gobierno no tiene solución", "dominante",
     "Transportistas, productores agropecuarios y sector informal", date(2026, 1, 12), 9.2),
    ("El MAS está fracturado y ya no puede gobernar con unidad", "dominante",
     "Analistas políticos, medios nacionales y oposición", date(2026, 1, 18), 8.8),
    ("La inseguridad ciudadana aumentó sin control en las principales ciudades", "dominante",
     "Vecinos organizados, medios locales y redes sociales", date(2026, 1, 25), 8.6),
    ("Bolivia tiene un potencial enorme que el gobierno no sabe aprovechar", "contrarrelato",
     "Sector privado, movimientos cívicos y juventud emprendedora", date(2026, 2, 3), 7.9),
    ("La corrupción en contratos de obras públicas llega hasta el gabinete", "emergente",
     "Periodismo de investigación y fiscalización parlamentaria", date(2026, 2, 7), 8.5),
    ("El Litio es Bolivia pero los contratos no benefician al pueblo", "dominante",
     "Movimientos sociales y comunidades del altiplano", date(2026, 1, 20), 8.1),
    ("El gobierno se habla solo mientras la gente sufre la crisis económica", "dominante",
     "Ciudadanía en redes sociales y radio comunitaria", date(2026, 2, 10), 8.9),
    ("Los movimientos sociales ya no respaldan al MAS como antes", "emergente",
     "Organizaciones sindicales y campesinas disidentes", date(2026, 2, 14), 8.3),
    ("La salud y la educación pública están en colapso en el interior del país", "dominante",
     "Comunidades rurales y organizaciones de base", date(2026, 1, 30), 8.7),
]
for txt, tipo, actor, fecha, peso in narrativas:
    db.add(Narrative(project_id=pid, texto=txt, tipo=tipo,
                     actor_politico=actor, fecha_deteccion=fecha, peso=peso))

# ── Emociones ─────────────────────────────────────────────────────────────
emociones = [
    # IRA — contra la gestión económica
    ("ira", 9.2, "Twitter/X",        date(2026, 1, 9),  "Pico de indignación tras publicación de índice de inflación enero 2026"),
    ("ira", 8.8, "Facebook",          date(2026, 1, 14), "Filas de horas en surtidores de gasolina — videos virales desde La Paz y Cochabamba"),
    ("ira", 9.1, "TikTok",            date(2026, 1, 19), "Videos de surtidores vacíos y camioneros varados con millones de vistas"),
    ("ira", 8.5, "Twitter/X",         date(2026, 1, 24), "Hashtag #BoliviaEnCrisis ocupa trending durante 48 horas"),
    ("ira", 9.3, "Facebook",          date(2026, 2, 4),  "Reacción masiva ante declaraciones del ministro de Economía"),
    ("ira", 8.7, "Instagram",         date(2026, 2, 9),  "Reels de protestas en El Alto con alta difusión nacional"),
    ("ira", 9.0, "Twitter/X",         date(2026, 2, 15), "Trending sobre nuevo caso de corrupción en ministerio de Obras Públicas"),
    ("ira", 8.4, "WhatsApp viral",    date(2026, 2, 20), "Cadenas sobre alza de precios de la canasta básica"),

    # MIEDO — inestabilidad y crisis
    ("miedo", 8.1, "Twitter/X",       date(2026, 1, 10), "Preocupación por el impacto del déficit fiscal en los programas sociales del Estado"),
    ("miedo", 7.8, "Facebook",         date(2026, 1, 17), "Incertidumbre sobre el acceso a crédito externo ante el deterioro de las finanzas públicas"),
    ("miedo", 8.4, "Telegram",         date(2026, 1, 23), "Cadenas sobre posible recorte de subsidios a combustibles y su impacto en el transporte"),
    ("miedo", 7.5, "WhatsApp viral",   date(2026, 1, 29), "Audios sobre crisis del gas natural y su impacto en exportaciones"),
    ("miedo", 8.0, "Twitter/X",        date(2026, 2, 5),  "Economistas advierten sobre el impacto del déficit fiscal en la calidad del gasto público"),
    ("miedo", 7.6, "TikTok",           date(2026, 2, 11), "Contenido viral sobre pérdida de empleos en sector informal"),
    ("miedo", 8.2, "Facebook",         date(2026, 2, 17), "Reacción a rebaja en calificación crediticia de Bolivia por Moody's"),

    # FRUSTRACIÓN — contra la clase política
    ("frustracion", 9.1, "Twitter/X",  date(2026, 1, 11), "Saturación de quejas sobre promesas no cumplidas del programa de gobierno"),
    ("frustracion", 8.9, "Facebook",   date(2026, 1, 16), "Grupos ciudadanos comparten memes sobre el contraste discurso-realidad"),
    ("frustracion", 9.3, "Instagram",  date(2026, 1, 22), "Historias virales sobre burocracia y tramitología en entidades estatales"),
    ("frustracion", 8.6, "TikTok",     date(2026, 1, 28), "Comparativos virales del tipo de vida de ministros vs ciudadanía"),
    ("frustracion", 9.0, "Twitter/X",  date(2026, 2, 6),  "Hashtag #YaBasta con alta actividad desde las seis ciudades capitales"),
    ("frustracion", 8.8, "YouTube",    date(2026, 2, 12), "Comentarios masivos en entrevistas a funcionarios negando la crisis"),
    ("frustracion", 9.2, "Facebook",   date(2026, 2, 18), "Viralización de reportaje sobre contratos irregulares en YPFB"),

    # ESPERANZA — señales débiles pero presentes
    ("esperanza", 4.5, "Facebook",     date(2026, 1, 13), "Reacciones positivas a anuncio de programa de empleo juvenil"),
    ("esperanza", 5.1, "Twitter/X",    date(2026, 1, 21), "Respaldo a iniciativa legislativa contra la corrupción"),
    ("esperanza", 5.8, "Instagram",    date(2026, 1, 27), "Cobertura positiva de avances en industrialización del litio"),
    ("esperanza", 6.2, "YouTube",      date(2026, 2, 3),  "Video de proyecto agropecuario con tecnología con amplia recepción"),
    ("esperanza", 5.5, "TikTok",       date(2026, 2, 8),  "Jóvenes emprendedores compartiendo historias de éxito a pesar de la crisis"),
    ("esperanza", 6.0, "Facebook",     date(2026, 2, 16), "Movilización ciudadana en torno a plataforma de transparencia nueva"),
    ("esperanza", 5.3, "Twitter/X",    date(2026, 2, 21), "Reacción positiva a acuerdo de inversión extranjera en sector energético"),

    # DESCONFIANZA — narrativa dominante nacional
    ("desconfianza", 9.0, "Twitter/X", date(2026, 1, 8),  "Escepticismo masivo ante datos oficiales del INE sobre crecimiento"),
    ("desconfianza", 8.7, "Facebook",  date(2026, 1, 15), "Comentarios desconfiados ante actos públicos del Ejecutivo"),
    ("desconfianza", 9.2, "Telegram",  date(2026, 1, 21), "Análisis ciudadano viral que cuestiona las cifras oficiales de crecimiento económico del INE"),
    ("desconfianza", 8.5, "Twitter/X", date(2026, 1, 26), "Reacción a nota de investigación sobre nepotismo en ministerios"),
    ("desconfianza", 9.1, "Instagram", date(2026, 2, 2),  "Infografías virales sobre inconsistencias entre discurso y presupuesto"),
    ("desconfianza", 8.9, "YouTube",   date(2026, 2, 9),  "Comentarios masivos en videos del presidente evitando preguntas difíciles"),
    ("desconfianza", 9.3, "Facebook",  date(2026, 2, 15), "Viralización de documento filtrado sobre deuda externa no declarada"),

    # ORGULLO — identidad nacional y recursos naturales
    ("orgullo", 6.8, "Instagram",     date(2026, 1, 18), "Contenido sobre riqueza natural y biodiversidad de Bolivia con alta interacción"),
    ("orgullo", 7.5, "TikTok",        date(2026, 1, 25), "Videos del carnaval de Oruro y festividades culturales con millones de vistas"),
    ("orgullo", 6.5, "Facebook",      date(2026, 2, 1),  "Comunidades de bolivianos en el exterior compartiendo contenido patriótico"),
    ("orgullo", 7.0, "Twitter/X",     date(2026, 2, 7),  "Debate sobre el potencial del litio activa sentimiento de soberanía nacional"),
    ("orgullo", 7.3, "YouTube",       date(2026, 2, 14), "Documental sobre la Chiquitanía y el Pantanal con alta difusión orgánica"),
]
for tipo, intens, fuente, fecha, notas in emociones:
    db.add(Emotion(project_id=pid, tipo=tipo, intensidad=intens,
                   fuente=fuente, fecha=fecha, notas=notas))

# ── Arquetipos ────────────────────────────────────────────────────────────
arquetipos = [
    ("El ciudadano urbano en crisis económica",
     "Hombre o mujer 28-50 años, ciudades capitales. Trabajador formal o informal golpeado por la inflación, el alza del costo de vida y la escasez de combustible. Su lealtad política es volátil — la define la situación económica del día a día.",
     28.0, "frustracion",
     ["Facebook", "WhatsApp", "Twitter/X"],
     "Estabilidad económica, empleo digno, combate a la inflación, mejora del poder adquisitivo",
     "Pérdida de empleo, mayor carestía de vida, recorte de subsidios, deterioro de servicios públicos"),
    ("El movimientista decepcionado",
     "Hombre o mujer 35-60 años, base social del MAS. Apoyó la revolución pero siente que la corrupción y las divisiones internas traicionaron los ideales del proceso de cambio. Su voto ya no es seguro.",
     22.0, "desconfianza",
     ["Radio comunitaria", "Facebook", "Boca a boca"],
     "Soberanía, justicia social, dignidad, proceso de cambio real",
     "Traición de dirigentes, corrupción interna, alejamiento de las bases"),
    ("El joven boliviano sin futuro local",
     "18-32 años, ciudades medianas y grandes. Alto consumo digital, alta frustración con las oportunidades de empleo y el contexto económico. El 40% considera emigrar. Muy activo en redes con contenido crítico.",
     20.0, "ira",
     ["TikTok", "Instagram", "Twitter/X", "YouTube"],
     "Meritocracia, empleo técnico, innovación, transparencia institucional",
     "Migración forzada, nepotismo, falta de oportunidades, hipocresía política"),
    ("El empresario y clase media urbana",
     "35-60 años, sector privado, comercio y servicios. Afectado por el déficit fiscal, la burocracia y la inseguridad jurídica. Migra hacia la oposición política. Alto poder de incidencia en medios.",
     18.0, "miedo",
     ["Twitter/X", "LinkedIn", "Medios digitales"],
     "Seguridad jurídica, estabilidad monetaria, libre mercado, estado de derecho",
     "Confiscación de propiedades, inseguridad, deterioro del entorno fiscal y macroeconómico"),
    ("El ciudadano rural e indígena olvidado",
     "Comunidades rurales, pueblos indígenas y áreas periurbanas. Históricamente base del MAS pero siente que las promesas del proceso de cambio no llegaron hasta su comunidad. Voz en radio y boca a boca.",
     12.0, "esperanza",
     ["Radio rural", "Boca a boca", "WhatsApp"],
     "Acceso a salud, agua potable, educación de calidad, reconocimiento cultural",
     "Olvido del gobierno central, extractivismo sin beneficio local, promesas vacías"),
]
for nombre, desc, peso, emocion, canales, valores, miedos in arquetipos:
    db.add(Archetype(project_id=pid, nombre=nombre, descripcion=desc,
                     peso_relativo=peso, emocion_dominante=emocion,
                     canales=canales, valores_clave=valores, miedos=miedos))

# ── Lenguaje (80 términos) ────────────────────────────────────────────────
lenguaje_data = [
    # CRISIS ECONÓMICA (12)
    ("el presupuesto en déficit","frase",   165, "economia",    "alto",  "Preocupación ciudadana por el déficit fiscal y su impacto en servicios públicos",  date(2026, 1, 8)),
    ("la inversión pública baja","frase",   172, "economia",    "alto",  "Percepción del recorte en obras e infraestructura por ajuste del presupuesto nacional", date(2026, 1, 9)),
    ("la inflación nos come",   "frase",   162, "economia",    "alto",  "Percepción del alza de precios en canasta básica como agresión al hogar",           date(2026, 1, 11)),
    ("el gas se terminó",       "frase",   148, "economia",    "alto",  "Percepción de agotamiento de las reservas de gas natural exportable del país",      date(2026, 1, 14)),
    ("el déficit fiscal sube",  "frase",   121, "economia",    "alto",  "Alarma ciudadana por el crecimiento del déficit fiscal del gobierno central",        date(2026, 1, 18)),
    ("el gas se acabó",         "frase",   156, "economia",    "alto",  "Crisis de producción de gas natural — caída exportaciones a Argentina y Brasil",    date(2026, 1, 22)),
    ("la estabilidad cambiaria", "frase",   94, "economia",    "bajo",  "Reconocimiento ciudadano de la estabilidad del tipo de cambio como logro del BCB", date(2026, 1, 26)),
    ("no alcanza el sueldo",    "frase",   171, "economia",    "alto",  "Expresión de la crisis de poder adquisitivo en trabajadores formales e informales",  date(2026, 2, 1)),
    ("el contrabando gana",     "frase",   112, "economia",    "alto",  "Referencia al mercado negro de combustibles y dólares como consecuencia",           date(2026, 2, 5)),
    ("YPFB en crisis",          "frase",   124, "economia",    "alto",  "Cuestionamiento a la empresa petrolera estatal por la crisis de combustibles",      date(2026, 2, 8)),
    ("el litio nos salva",      "frase",    97, "economia",    "medio", "Esperanza puesta en la industrialización del litio como salida a la crisis",        date(2026, 2, 12)),
    ("la deuda se dispara",     "frase",   108, "economia",    "alto",  "Alarma por el crecimiento de la deuda externa boliviana",                           date(2026, 2, 16)),

    # POLÍTICA Y PODER (12)
    ("el MAS dividido",         "frase",   167, "desconfianza","alto",  "Fractura interna entre arcistas y evistas como narrativa dominante",               date(2026, 1, 8)),
    ("el arco y la flecha",     "simbolo", 143, "identidad",   "alto",  "Símbolo del MAS — usado irónicamente por críticos y nostálgicamente por bases",    date(2026, 1, 12)),
    ("el proceso de cambio",    "frase",   156, "desconfianza","alto",  "Concepto fundacional del MAS — ahora usado con escepticismo o ironía",             date(2026, 1, 16)),
    ("el evismo vs el arcismo", "frase",   138, "desconfianza","alto",  "Nominación popular de la fractura interna del partido de gobierno",                date(2026, 1, 20)),
    ("la rosca volvió",         "frase",   122, "desconfianza","alto",  "Acusación cruzada entre facciones de que el adversario representa a las élites",    date(2026, 1, 24)),
    ("el gobierno de turno",    "frase",   131, "desconfianza","medio", "Distanciamiento ciudadano de la figura del gobierno actual",                        date(2026, 1, 28)),
    ("la oposición unida",      "frase",    97, "activacion",  "medio", "Expectativa sobre una posible coalición opositora para 2027",                      date(2026, 2, 2)),
    ("ni Evo ni Arce",          "meme",    118, "indecision",  "alto",  "Rechazo ciudadano a ambas figuras del MAS — señal de agotamiento político",        date(2026, 2, 6)),
    ("el golpe blando",         "frase",    84, "espanto",     "medio", "Término usado por el gobierno para describir movimientos opositores",               date(2026, 2, 10)),
    ("el pueblo manda",         "frase",    93, "activacion",  "alto",  "Slogan del MAS — reapropriado irónicamente por la oposición ciudadana",             date(2026, 2, 14)),
    ("la asamblea legislativa", "frase",    76, "gestion",     "bajo",  "Referencia al poder legislativo como espacio de bloqueo político",                  date(2026, 2, 18)),
    ("el tribunal electoral",   "frase",    88, "desconfianza","medio", "Cuestionamiento a la independencia del TSE ante elecciones de 2027",               date(2026, 2, 21)),

    # COMBUSTIBLE Y SERVICIOS (10)
    ("la cola del surtidor",    "frase",   189, "emocion",     "alto",  "Imagen viral de filas de horas para comprar gasolina — icono de la crisis 2026",   date(2026, 1, 10)),
    ("sin gasolina no hay comida","frase", 172, "economia",    "alto",  "Cadena causal entre crisis de combustibles y desabastecimiento alimentario",        date(2026, 1, 13)),
    ("el diesel para el campo", "frase",   148, "economia",    "alto",  "Demanda del sector agropecuario de garantizar combustible para la cosecha",        date(2026, 1, 17)),
    ("apagones otra vez",       "frase",   134, "gestion",     "alto",  "Cortes de electricidad recurrentes — señal de falla sistémica del sector eléctrico",date(2026, 1, 21)),
    ("el gas de cañería",       "frase",   119, "economia",    "alto",  "Crisis del GLP domiciliario en La Paz y El Alto — afecta cocción de alimentos",    date(2026, 1, 25)),
    ("el transporte paralizado","frase",   156, "gestion",     "alto",  "Bloqueos de transportistas exigiendo combustible y revisión de tarifas",            date(2026, 2, 3)),
    ("el internet caro y lento","frase",    98, "gestion",     "medio", "Comparativo Bolivia vs región en calidad y precio de conectividad digital",         date(2026, 2, 7)),
    ("el hospital sin medicamentos","frase",143,"gestion",     "alto",  "Crisis de abastecimiento en hospitales públicos — recurrente en redes",             date(2026, 2, 11)),
    ("agua o no hay",           "frase",   112, "gestion",     "alto",  "Crisis hídrica en ciudades del sur y valles — gestión deficiente denunciada",      date(2026, 2, 15)),
    ("los mercados se vacían",  "frase",   127, "economia",    "alto",  "Percepción de desabastecimiento en mercados populares de las ciudades capitales",   date(2026, 2, 19)),

    # INSEGURIDAD Y ORDEN (8)
    ("la inseguridad se desbordó","frase", 165, "espanto",     "alto",  "Percepción de aumento de robos, asaltos y crimen organizado en ciudades capitales",date(2026, 1, 9)),
    ("el narcotráfico avanza",  "frase",   148, "espanto",     "alto",  "Alarma por expansión de rutas y estructuras del narcotráfico en Bolivia",           date(2026, 1, 15)),
    ("la policía no llega",     "frase",   132, "gestion",     "alto",  "Crítica a la respuesta policial ante emergencias ciudadanas — impunidad",           date(2026, 1, 20)),
    ("los femicidios aumentan", "frase",   138, "espanto",     "alto",  "Datos sobre violencia de género como falla sistémica del Estado",                   date(2026, 1, 26)),
    ("el crimen organizado",    "frase",   119, "espanto",     "alto",  "Referencia a estructuras criminales con posible colusión política",                  date(2026, 2, 2)),
    ("fuerza pública militarizada","frase", 87, "espanto",     "medio", "Preocupación por uso de fuerzas militares en conflictos sociales",                   date(2026, 2, 8)),
    ("me robaron y nada pasó",  "frase",   104, "espanto",     "alto",  "Expresión de impunidad y abandono ciudadano ante la delincuencia",                  date(2026, 2, 13)),
    ("Bolivia tierra de nadie", "frase",   124, "espanto",     "alto",  "Hipérbole ciudadana que expresa la percepción de colapso del orden público",        date(2026, 2, 18)),

    # IDENTIDAD Y SOBERANÍA (8)
    ("soberanía nacional",      "frase",   112, "identidad",   "alto",  "Valor fundacional invocado tanto por el gobierno como por la oposición",            date(2026, 1, 12)),
    ("el litio es boliviano",   "frase",   134, "identidad",   "alto",  "Demanda de que el litio beneficie soberanamente al pueblo boliviano",               date(2026, 1, 19)),
    ("el pueblo multicolor",    "simbolo",  89, "identidad",   "medio", "Referencia a la diversidad étnica y cultural de Bolivia como fortaleza",            date(2026, 1, 27)),
    ("la wiphala",              "simbolo",  97, "identidad",   "alto",  "Símbolo de los pueblos originarios — su uso político sigue generando debate",       date(2026, 2, 4)),
    ("Bolivia para los bolivianos","frase",118,"identidad",   "alto",  "Slogan de soberanía usado ante presencia de inversión extranjera",                   date(2026, 2, 9)),
    ("la salteña y el pan",     "simbolo",  76, "identidad",   "medio", "Metáfora de la identidad cotidiana ante la carestía — humor resignado",             date(2026, 2, 13)),
    ("el camino del inca",      "frase",    63, "identidad",   "bajo",  "Referencia histórica usada en narrativas de orgullo cultural prehispánico",         date(2026, 2, 17)),
    ("más boliviano que nunca", "frase",    88, "identidad",   "alto",  "Expresión de arraigo ante la crisis — orgullo defensivo",                          date(2026, 2, 21)),

    # DESCONFIANZA INSTITUCIONAL (10)
    ("la justicia no existe",   "frase",   167, "desconfianza","alto",  "Percepción de inexistencia de un sistema judicial independiente",                   date(2026, 1, 8)),
    ("compran al juez",         "frase",   143, "desconfianza","alto",  "Percepción de corrupción endémica en el poder judicial",                            date(2026, 1, 14)),
    ("los datos son mentira",   "frase",   134, "desconfianza","alto",  "Desconfianza total en estadísticas oficiales del INE y el gobierno",                date(2026, 1, 20)),
    ("el censo fue amañado",    "frase",   128, "desconfianza","alto",  "Cuestionamiento a los resultados del censo de 2024 y su impacto en recursos",       date(2026, 1, 25)),
    ("vienen cada 5 años",      "frase",   119, "desconfianza","alto",  "Crítica al oportunismo electoral — el gobierno sólo recuerda al pueblo en campaña", date(2026, 2, 1)),
    ("el TSE no es confiable",  "frase",   104, "desconfianza","alto",  "Cuestionamiento a la independencia del tribunal electoral de cara a 2027",          date(2026, 2, 6)),
    ("eso no sale en la tele",  "meme",    112, "desconfianza","alto",  "Referencia a censura o autocensura mediática en canales oficiales o afines",        date(2026, 2, 11)),
    ("los medios mienten",      "frase",    96, "desconfianza","medio", "Desconfianza extendida en medios tanto gubernamentales como privados",               date(2026, 2, 15)),
    ("la encuesta la compraron","frase",    83, "desconfianza","medio", "Desconfianza en sondeos de intención de voto y aprobación presidencial",             date(2026, 2, 18)),
    ("nadie rinde cuentas",     "frase",   128, "desconfianza","alto",  "Expresión de falta de accountability en todos los niveles del Estado",              date(2026, 2, 21)),

    # ACTIVACIÓN CIUDADANA (10)
    ("no más silencio",         "frase",   138, "activacion",  "alto",  "Llamado a la denuncia pública y la movilización ciudadana",                         date(2026, 1, 10)),
    ("el voto en 2027",         "frase",   119, "activacion",  "alto",  "Referencia a las elecciones generales de 2027 como momento de cambio",             date(2026, 1, 16)),
    ("que se vayan todos",      "meme",    148, "activacion",  "alto",  "Expresión de rechazo total a la clase política — reminiscente de Argentina 2001",   date(2026, 1, 22)),
    ("la marcha va",            "frase",   124, "activacion",  "alto",  "Convocatoria a marchas y protestas — muy frecuente en redes sociales bolivianas",   date(2026, 1, 27)),
    ("fiscalicemos juntos",     "frase",    93, "activacion",  "medio", "Llamado a la ciudadanía para monitorear la gestión gubernamental",                   date(2026, 2, 3)),
    ("el poder es nuestro",     "frase",   107, "activacion",  "alto",  "Apropiación ciudadana del discurso de soberanía popular",                           date(2026, 2, 7)),
    ("ya basta de corrupción",  "frase",   134, "activacion",  "alto",  "Slogan anticorrupción más utilizado en protestas y redes",                          date(2026, 2, 11)),
    ("Bolivia que despierta",   "frase",    86, "activacion",  "medio", "Narrativa de despertar ciudadano ante la crisis — impulso cívico",                  date(2026, 2, 15)),
    ("acción ciudadana ya",     "frase",    97, "activacion",  "alto",  "Llamado a la participación activa más allá del voto",                               date(2026, 2, 19)),
    ("cambiemos nosotros",      "frase",    79, "activacion",  "medio", "Discurso de empoderamiento ciudadano ante inacción gubernamental",                  date(2026, 2, 22)),
]

for termino, tipo, freq, func, impacto, contexto, fecha in lenguaje_data:
    db.add(LanguageCode(
        project_id=pid, termino=termino, tipo=tipo,
        frecuencia=freq, funcion_cultural=func,
        impacto_voto_blando=impacto, contexto=contexto,
        fecha_deteccion=fecha
    ))

# ── Comunidades digitales ─────────────────────────────────────────────────
comunidades = [
    ("Facebook",    "Bolivia en Crisis — Noticias y Análisis",    "polarizado",    145000,
     "Megagrupo nacional de alta actividad. Centro de viralización de narrativas críticas al gobierno. Mezcla de ciudadanía activa, periodistas y operadores políticos de todas las tendencias.", 9),
    ("Twitter/X",   "Periodistas e Intelectuales Bolivia",        "amplificador",   28000,
     "Red de formadores de opinión. Bajo volumen pero muy alto impacto en agenda mediática nacional e internacional. Tienen acceso a tomadores de decisión.", 9),
    ("TikTok",      "Generación Z Bolivia — Política y Crisis",   "activo",         87000,
     "Jóvenes creadores de contenido con enfoque político. Alta capacidad de viralización. El humor negro y la crítica ácida son sus formatos dominantes.", 8),
    ("WhatsApp",    "Redes sindicales y organizaciones de base",  "silencioso",    320000,
     "Canal de transmisión masiva de mensajes políticos en sectores organizados. Muy difícil de monitorear pero con altísima penetración en zonas rurales y periurbanas.", 9),
    ("YouTube",     "Medios digitales independientes Bolivia",    "amplificador",   64000,
     "Canales de noticias y análisis político. Crecimiento exponencial ante desconfianza en medios tradicionales. Muy influyentes en El Alto, La Paz y Cochabamba.", 8),
    ("Telegram",    "Canales de información política Bolivia",    "amplificador",   41000,
     "Canales de filtraciones, investigación y análisis. Operan con anonimato. Alta credibilidad entre el público informado y los periodistas.", 8),
    ("Radio",       "Audiencia Radios AM y FM Bolivia",           "silencioso",    890000,
     "El medio de mayor penetración nacional, especialmente en áreas rurales e indígenas. Mensajes en castellano y lenguas originarias (aymara, quechua). Canal decisivo para el voto rural.", 9),
    ("Facebook",    "Empresarios y Clase Media Bolivia",          "activo",         52000,
     "Red del sector privado y profesionales. Alta influencia en narrativas económicas. Muy críticos de la gestión gubernamental y con poder de presión económica.", 8),
]
for plat, nombre, tipo, tam, desc, inf in comunidades:
    db.add(Community(project_id=pid, plataforma=plat, nombre_grupo=nombre,
                     tipo=tipo, tamanio_estimado=tam, descripcion=desc, influencia=inf))

# ── Riesgos ───────────────────────────────────────────────────────────────
riesgos = [
    ("Caída en exportaciones de gas natural reduce ingresos fiscales del Estado",
     "La producción de gas natural sigue en declive, reduciendo los ingresos por exportaciones a Argentina y Brasil. El gobierno enfrenta mayor presión para ajustar el presupuesto de inversión pública.",
     "rojo", 5, date(2026, 2, 19)),
    ("Escasez crítica de combustibles paraliza sector productivo",
     "La falta de diesel y gasolina amenaza la cosecha de soya y la cadena de abastecimiento alimentario. El sector transporte anuncia bloqueos indefinidos si no hay respuesta en 72 horas.",
     "rojo", 5, date(2026, 2, 17)),
    ("Filtración de contratos irregulares en ministerio de Obras Públicas",
     "Documentos revelados por periodismo de investigación muestran sobreprecios del 60% en contratos de infraestructura vial. La oposición prepara interpelación en la Asamblea.",
     "rojo", 4, date(2026, 2, 15)),
    ("Movilización de movimientos sociales contra el gobierno",
     "Organizaciones sindicales y campesinas convocaron a marcha nacional para el 5 de marzo. La fractura dentro del MAS les da legitimidad a ambos bandos. Riesgo de bloqueos prolongados.",
     "amarillo", 4, date(2026, 2, 12)),
    ("Déficit fiscal creciente presiona la inversión social del gobierno",
     "El déficit del sector público supera el 8% del PIB. El gobierno enfrenta la disyuntiva entre mantener subsidios, aumentar la deuda o reducir la inversión en salud y educación.",
     "amarillo", 4, date(2026, 2, 10)),
    ("Oposición política se articula en coalición para 2027",
     "Líderes de Comunidad Ciudadana, Creemos y nuevos movimientos cívicos iniciaron conversaciones para una candidatura única. Si se consolida, cambia el escenario electoral.",
     "amarillo", 3, date(2026, 2, 8)),
    ("Crisis hídrica en ciudades del sur del país",
     "Cochabamba, Sucre y Potosí reportan cortes de agua de hasta 20 horas diarias. El gobierno nacional no ha emitido declaratoria de emergencia.",
     "amarillo", 3, date(2026, 2, 6)),
    ("Campaña de desinformación sobre el litio y contratos extranjeros",
     "Cuentas coordinadas difunden información falsa sobre condiciones de los contratos de litio con empresas chinas y rusas. Genera desconfianza en la gestión del recurso.",
     "verde", 2, date(2026, 2, 20)),
]
for tema, desc, nivel, vel, fecha in riesgos:
    db.add(Risk(project_id=pid, tema=tema, descripcion=desc,
                nivel=nivel, velocidad_crecimiento=vel,
                fecha_deteccion=fecha, activo=True))

db.commit()
db.close()

print("✓ Gobierno Nacional Bolivia cargado exitosamente.")
print(f"  Proyecto ID:   {pid}")
print(f"  Narrativas:    {len(narrativas)}")
print(f"  Emociones:     {len(emociones)}")
print(f"  Arquetipos:    {len(arquetipos)}")
print(f"  Lenguaje:      {len(lenguaje_data)} términos")
print(f"  Comunidades:   {len(comunidades)}")
print(f"  Riesgos:       {len(riesgos)}")
