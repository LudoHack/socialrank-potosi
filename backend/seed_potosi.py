"""
Seed de datos — Potosí: Minería, Litio y Territorio 2026
Monitoreo etnográfico digital del Departamento de Potosí
Sistema de análisis de percepción ciudadana, narrativas dominantes y riesgos políticos
Ejecutar: python seed_potosi.py
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
    nombre="Monitoreo Digital Potosí 2026 — Minería, Litio y Territorio",
    cliente="Social Rank Bolivia — Potosí",
    contexto_pais="Bolivia",
    fecha_inicio=date(2026, 1, 1),
    descripcion="Análisis etnográfico digital del Departamento de Potosí. Monitoreo de percepción ciudadana en torno a la crisis del Cerro Rico, la industrialización del litio en el Salar de Uyuni, los movimientos cívicos de COMCIPO, la contaminación hídrica y las tensiones entre cooperativistas, comunidades y el Estado. El departamento más pobre de Bolivia que concentra las mayores reservas de litio del mundo."
)
db.add(proyecto)
db.flush()
pid = proyecto.id

# ── Narrativas ────────────────────────────────────────────────────────────
narrativas = [
    ("El Cerro Rico se hunde y sus mineros mueren de silicosis mientras el Estado mira para otro lado",
     "dominante",
     "Mineros cooperativistas, familias del cerro, organizaciones de salud y ONG internacionales",
     date(2026, 1, 6), 9.6),

    ("500 años de saqueo y Potosí sigue siendo el departamento más pobre de Bolivia",
     "dominante",
     "Movimientos cívicos, COMCIPO, ciudadanía potosina y activistas culturales",
     date(2026, 1, 9), 9.3),

    ("China se lleva el litio del Salar de Uyuni y Potosí no verá un centavo más que antes",
     "dominante",
     "Comunidades del salar, COMCIPO, universitarios y opositores al gobierno",
     date(2026, 1, 14), 9.1),

    ("El río Pilcomayo y el agua de Potosí están envenenados por los metales pesados de las minas",
     "dominante",
     "Comunidades rurales, organizaciones ambientalistas y medios locales de salud",
     date(2026, 1, 18), 8.9),

    ("COMCIPO sale de nuevo a las calles porque el gobierno incumplió todos los acuerdos firmados",
     "dominante",
     "COMCIPO, juntas vecinales, gremios y ciudadanía movilizada de Potosí",
     date(2026, 1, 22), 8.8),

    ("Los cooperativistas se matan entre ellos por el Cerro Rico mientras los jóvenes se van de Potosí",
     "dominante",
     "Medios locales, familias afectadas y organizaciones de derechos humanos",
     date(2026, 1, 27), 8.6),

    ("La mina San Cristóbal de Sumitomo extrae el zinc y deja el altiplano sin agua",
     "emergente",
     "Comunidades del altiplano potosino, agricultores y activistas ambientales",
     date(2026, 2, 3), 8.4),

    ("Los jóvenes potosinos emigran a Argentina y Chile porque no hay futuro en el cerro",
     "emergente",
     "Jóvenes universitarios, familias con hijos emigrantes y radios comunitarias",
     date(2026, 2, 8), 8.2),

    ("YLB no cumple las metas de producción de litio y el contrato con China genera más dudas",
     "dominante",
     "Analistas económicos, periodistas de investigación y opositores al MAS",
     date(2026, 2, 12), 8.0),

    ("El litio del Salar de Uyuni puede sacar a Potosí de la pobreza si se maneja con soberanía real",
     "contrarrelato",
     "Gobierno nacional, YLB, sector pro-industrialización y movimientos indígenas aliados al MAS",
     date(2026, 2, 5), 7.1),
]
for txt, tipo, actor, fecha, peso in narrativas:
    db.add(Narrative(project_id=pid, texto=txt, tipo=tipo,
                     actor_politico=actor, fecha_deteccion=fecha, peso=peso))

# ── Emociones ─────────────────────────────────────────────────────────────
emociones = [
    # IRA — contra el Estado, las cooperativas y el extractivismo
    ("ira", 9.5, "Facebook",       date(2026, 1, 7),  "Viralización de video de minero con silicosis avanzada que no puede caminar — 3 millones de vistas en Bolivia"),
    ("ira", 9.2, "TikTok",         date(2026, 1, 12), "Videos del derrumbe visible en la cima del Cerro Rico — trending nacional con #CerroRicoSeMuere"),
    ("ira", 9.0, "WhatsApp viral", date(2026, 1, 19), "Cadena masiva sobre niños trabajando en socavones — difundida por organizaciones de derechos del niño"),
    ("ira", 8.8, "Facebook",       date(2026, 1, 25), "Reacción ante declaraciones del Ministro de Minería minimizando el colapso estructural del cerro"),
    ("ira", 9.1, "Twitter/X",      date(2026, 2, 4),  "Hashtag #LitioParaPotosi tras filtrarse cláusulas del contrato YLB-CATL consideradas desfavorables"),
    ("ira", 8.6, "Facebook",       date(2026, 2, 9),  "Fotos virales de río Pilcomayo con espuma naranja de drenaje ácido de minas — miles de compartidos"),
    ("ira", 9.3, "TikTok",         date(2026, 2, 16), "Minero cooperativista documenta disputa con dinamita en bocamina — video restringido pero replicado"),
    ("ira", 8.9, "Twitter/X",      date(2026, 2, 21), "Trending #ComcipoTieneRazon tras confirmar que aeropuerto prometido en 2010 sigue sin construirse"),

    # MIEDO — colapso, silicosis, agua, inestabilidad
    ("miedo", 9.4, "Facebook",     date(2026, 1, 8),  "Pánico en barrios de Potosí ciudad ante reportes de grietas en viviendas sobre galerías del cerro"),
    ("miedo", 8.7, "WhatsApp viral",date(2026, 1, 15),"Audios sobre posible colapso súbito de zona norte del Cerro Rico — difundidos por mineros en servicio"),
    ("miedo", 8.9, "TikTok",       date(2026, 1, 21), "Video viral de minero tosiendo sangre — silicosis en estadio terminal. 5 millones de reproducciones"),
    ("miedo", 8.4, "Facebook",     date(2026, 1, 29), "Madres de Potosí expresan miedo de que sus hijos beban agua contaminada por plomo y arsénico"),
    ("miedo", 8.6, "Radio/YouTube",date(2026, 2, 6),  "Informe de geólogos advierte que la cota 4,400 msnm del cerro puede colapsar en los próximos años"),
    ("miedo", 8.2, "WhatsApp viral",date(2026, 2, 13),"Cadenas sobre supuesta contaminación del acuífero del Salar de Uyuni por plantas piloto de litio"),
    ("miedo", 8.5, "Twitter/X",    date(2026, 2, 20), "Analistas advierten sobre posible desempleo masivo si ceierran bocaminas del Cerro Rico por seguridad"),

    # FRUSTRACIÓN — incumplimientos, pobreza histórica, migración
    ("frustracion", 9.4, "Facebook",  date(2026, 1, 10), "Listado viral de los 14 acuerdos firmados por gobiernos sucesivos con COMCIPO y nunca cumplidos"),
    ("frustracion", 9.1, "TikTok",    date(2026, 1, 17), "Jóvenes comparan ingreso de minero boliviano vs. chileno — diferencia de 10 a 1 en sueldos"),
    ("frustracion", 9.3, "WhatsApp viral",date(2026, 1, 24),"Cifras del INE confirmando que Potosí sigue siendo el departamento con mayor pobreza extrema de Bolivia"),
    ("frustracion", 8.9, "Facebook",  date(2026, 1, 31), "Meme viral: foto de la Casa de la Moneda colonial vs. foto de barrio sin agua de Potosí 2026"),
    ("frustracion", 9.0, "Twitter/X", date(2026, 2, 7),  "Universitarios de la UATF denuncian que carreras mineras no tienen laboratorios ni equipamiento actualizado"),
    ("frustracion", 8.8, "YouTube",   date(2026, 2, 14), "Documental corto sobre minero que trabajó 20 años en el cerro y no tiene jubilación ni seguro médico"),
    ("frustracion", 9.2, "Facebook",  date(2026, 2, 19), "Viralización de estadística: Potosí produce 30% de los minerales de Bolivia y recibe 8% del presupuesto nacional"),

    # ESPERANZA — litio soberano, turismo, jóvenes emprendedores
    ("esperanza", 6.8, "Facebook",    date(2026, 1, 13), "Reacciones positivas a anuncio de planta de procesamiento de litio en territorio potosino"),
    ("esperanza", 7.2, "YouTube",     date(2026, 1, 20), "Documental sobre jóvenes potosinos creando empresa de turismo minero — miles de reproducciones positivas"),
    ("esperanza", 6.5, "TikTok",      date(2026, 1, 26), "Contenido viral sobre biodiversidad del Salar de Uyuni — potencial turístico generando orgullo"),
    ("esperanza", 7.4, "Instagram",   date(2026, 2, 2),  "Fotos de la arquitectura colonial de Potosí ciudad generan turismo digital — comunidad orgullosa"),
    ("esperanza", 6.1, "Facebook",    date(2026, 2, 11), "Anuncio de proyecto de agua potable para comunidades mineras del Cerro Rico recibe apoyo ciudadano"),
    ("esperanza", 6.9, "Twitter/X",   date(2026, 2, 18), "Noticia de jóvenes potosinos seleccionados para programa de becas en ingeniería minera en el exterior"),

    # DESCONFIANZA — contratos, YLB, COMIBOL, Estado
    ("desconfianza", 9.0, "Twitter/X",  date(2026, 1, 9),  "Escepticismo masivo ante datos oficiales de YLB sobre producción real de carbonato de litio"),
    ("desconfianza", 8.8, "Telegram",   date(2026, 1, 16), "Filtración de cláusula del contrato YLB-CATL que otorga mayoría a empresa china — análisis viral"),
    ("desconfianza", 9.1, "Facebook",   date(2026, 1, 22), "Ciudadanos potosinos cuestionan que las regalías mineras lleguen efectivamente al departamento"),
    ("desconfianza", 8.5, "Twitter/X",  date(2026, 1, 30), "Investigación periodística sobre corrupción en contratos de COMIBOL con cooperativas del Cerro Rico"),
    ("desconfianza", 9.2, "Facebook",   date(2026, 2, 5),  "Infografía viral: Potosí tiene 50% de las reservas de litio del mundo y 55% de pobreza extrema"),
    ("desconfianza", 8.7, "Telegram",   date(2026, 2, 12), "Documento filtrado que muestra que mina San Cristóbal (Sumitomo) pagó menos regalías de lo declarado"),
    ("desconfianza", 9.3, "Facebook",   date(2026, 2, 20), "Comparativa viral: regalías que recibe Chile de su litio vs regalías que recibe Potosí — diferencia abismal"),

    # ORGULLO — identidad potosina, Cerro Rico como símbolo, historia
    ("orgullo", 8.2, "TikTok",    date(2026, 1, 11), "Videos del Cerro Rico al atardecer con música andina — millones de vistas internacionales — identidad"),
    ("orgullo", 7.8, "Facebook",  date(2026, 1, 18), "Comunidades potosinas compartiendo imágenes de la Casa de la Moneda — orgullo patrimonial"),
    ("orgullo", 7.5, "Instagram", date(2026, 1, 25), "Fotos del Carnaval de Potosí y la ch'alla minera — rituales al Tío del Cerro con alta resonancia cultural"),
    ("orgullo", 8.0, "YouTube",   date(2026, 2, 1),  "Documental internacional sobre Potosí llega a 10 millones de vistas — potosinos lo comparten masivamente"),
    ("orgullo", 7.3, "TikTok",    date(2026, 2, 10), "Trend viral: 'Potosí fue el centro del mundo' — jóvenes hacen contenido con fotos históricas del esplendor"),
    ("orgullo", 8.4, "Facebook",  date(2026, 2, 17), "Comunidades de potosinos en Argentina comparten contenido del cerro — nostalgia y orgullo en la diáspora"),
]
for tipo, intens, fuente, fecha, notas in emociones:
    db.add(Emotion(project_id=pid, tipo=tipo, intensidad=intens,
                   fuente=fuente, fecha=fecha, notas=notas))

# ── Arquetipos ────────────────────────────────────────────────────────────
arquetipos = [
    ("El minero cooperativista del Cerro Rico",
     "Hombre 25-55 años. Trabaja en los socavones del Cerro Rico como miembro de una cooperativa. Tiene conciencia plena del riesgo de silicosis pero no tiene alternativa económica. Su identidad está profundamente fusionada con el cerro: es su sustento y su sentencia de muerte a la vez. Desconfía del Estado y de COMIBOL, pero tampoco confía completamente en los dirigentes cooperativistas que lucran a costa de él. Accede a noticias por Facebook y radio. Su lealtad política es pragmática: apoya a quien le garantice acceso al cerro.",
     30.0, "miedo",
     ["Facebook", "WhatsApp", "Radio Potosí"],
     "Acceso libre a las bocaminas, pensión de invalidez, ventilación en socavones, medicamentos para silicosis",
     "Derrumbes, silicosis acelerada, cierre de cooperativa, conflictos violentos con otras cooperativas, reforma que les quite derechos sobre el cerro"),

    ("El militante cívico de COMCIPO",
     "Hombre o mujer 35-65 años, arraigado en Potosí ciudad. Comerciante, profesional, dirigente barrial o universitario. Su identidad política se construye sobre el agravio histórico: Potosí da y el Estado no devuelve. Sigue a COMCIPO con convicción y es movilizador en su entorno. Mantiene listas de los acuerdos incumplidos por cada gobierno. Es escéptico de todos los partidos, incluida la oposición nacional. Su eje no es ideológico sino territorial: Potosí primero.",
     22.0, "frustracion",
     ["Facebook", "WhatsApp grupos cívicos", "Radio Illimani", "YouTube"],
     "Aeropuerto internacional, hospital de 4to nivel, industrialización del litio en Potosí, más regalías, agua potable para el departamento",
     "Que el litio se procese fuera de Potosí, nuevos incumplimientos del Estado, cooptación de COMCIPO por partidos políticos, pérdida de influencia de la sociedad civil"),

    ("El joven potosino que considera emigrar",
     "18-32 años, ciudades de Potosí, Tupiza o Villazón. Alto consumo digital (TikTok, Instagram, YouTube), frustración acumulada con la falta de oportunidades de empleo formal. El 40% de los jóvenes potosinos ya tiene familiares en Argentina o Chile. Ve el cerro como un destino de último recurso, no como una opción de vida. Ambivalente entre orgullo cultural y desesperanza. Muy crítico en redes, pero políticamente desafecto.",
     20.0, "frustracion",
     ["TikTok", "Instagram", "YouTube", "WhatsApp"],
     "Empleo formal, carrera profesional, internet de calidad, universidad con laboratorios, oportunidad sin tener que emigrar",
     "Terminar en el cerro como sus padres, silicosis, violencia de cooperativas, migración forzada, corrupción sin fin"),

    ("La mujer de la comunidad del Salar de Uyuni",
     "Mujer 25-55 años, comunidades originarias circundantes al Salar de Uyuni (Colcha K, Llica, Tahua). Su comunidad lleva décadas reclamando participación real en los beneficios del litio. Habla quechua o aymara, accede a información principalmente por radio y WhatsApp. Desconfía tanto de YLB como de las empresas chinas. Su preocupación central es el agua: el acuífero del que depende su comunidad puede verse afectado por la extracción masiva de salmuera.",
     15.0, "desconfianza",
     ["Radio comunitaria", "WhatsApp", "Boca a boca"],
     "Participación real en las regalías del litio, protección del acuífero, empleo en la planta para gente de la comunidad, respeto a la cosmovisión andina y la Pachamama",
     "Contaminación del agua del salar, desplazamiento comunitario, ser ignorada en los contratos, pérdida de acceso a la tierra"),

    ("El dirigente cooperativista con poder económico",
     "Hombre 40-65 años. Dirigente de cooperativa o propietario de varias bocaminas en el Cerro Rico. Tiene poder económico acumulado pero opera en la informalidad legal. Su relación con el Estado es transaccional: apoya al gobierno que le garantice acceso a las áreas que quiere explotar. Es el actor que bloquea las reformas de seguridad y salud en el cerro porque aumentarían sus costos. Tiene influencia sobre cientos de mineros y puede movilizarlos política o laboralmente.",
     13.0, "desconfianza",
     ["Facebook", "WhatsApp privado", "Reuniones presenciales"],
     "Acceso a nuevas áreas de COMIBOL para explotar, régimen fiscal favorable, bloquear auditorías ambientales, mantener el statu quo cooperativista",
     "Reforma que obligue a contratos laborales formales para peones, cierre de bocaminas por seguridad, investigación penal por condiciones de trabajo, pérdida de influencia sobre FENCOMIN"),
]
for nombre, desc, peso, emocion, canales, valores, miedos in arquetipos:
    db.add(Archetype(project_id=pid, nombre=nombre, descripcion=desc,
                     peso_relativo=peso, emocion_dominante=emocion,
                     canales=canales, valores_clave=valores, miedos=miedos))

# ── Lenguaje (70 términos) ─────────────────────────────────────────────────
lenguaje_data = [
    # MINERÍA Y CERRO RICO (12)
    ("el cerro se hunde",           "frase",   198, "mineria",    "alto",  "Referencia directa al hundimiento documentado de la cima del Cerro Rico de Potosí",                    date(2026, 1, 6)),
    ("la silicosis te mata",        "frase",   187, "mineria",    "alto",  "Conciencia extendida de la enfermedad pulmonar endémica entre mineros del Cerro Rico",                  date(2026, 1, 8)),
    ("el Tío del Cerro",            "simbolo", 165, "identidad",  "alto",  "Deidad andina de la mina — figura ritual central en la cosmovisión minera potosina. La ch'alla al Tío", date(2026, 1, 9)),
    ("el polvo del cerro nos come", "frase",   172, "mineria",    "alto",  "Expresión coloquial de la silicosis — el polvo de sílice como agente mortal cotidiano",                date(2026, 1, 11)),
    ("la bocamina 30",              "frase",   143, "mineria",    "alto",  "Referencia a bocaminas específicas como territorios disputados entre cooperativas rivales",             date(2026, 1, 14)),
    ("el dinamitazo",               "frase",   128, "mineria",    "alto",  "Explosiones con dinamita — tanto herramienta de trabajo como arma en conflictos entre cooperativas",   date(2026, 1, 17)),
    ("la palliri",                  "termino", 118, "mineria",    "medio", "Mujer que separa el mineral a mano fuera del socavón — figura histórica y actual del trabajo minero",   date(2026, 1, 20)),
    ("el cooperativista sin derechos","frase", 134, "mineria",    "alto",  "Tensión estructural: el cooperativista es nominalmente 'socio' pero sin jubilación ni seguro",         date(2026, 1, 22)),
    ("el Cerro Rico muere con nosotros","frase",156,"mineria",   "alto",  "Narrativa identitaria de co-destino entre el cerro y la comunidad minera — profunda carga simbólica",   date(2026, 1, 25)),
    ("Sumaj Orcko",                 "simbolo", 142, "identidad",  "alto",  "Nombre quechua del Cerro Rico ('cerro hermoso') — usado en discursos de orgullo e identidad",          date(2026, 1, 27)),
    ("el mineral a pulso",          "frase",   109, "mineria",    "medio", "Referencia al trabajo manual sin maquinaria — condiciones primitivas de extracción en socavones",       date(2026, 1, 30)),
    ("sin bocamina no hay familia", "frase",   138, "mineria",    "alto",  "Dependencia económica total de la familia en la actividad minera como único sustento",                  date(2026, 2, 2)),

    # LITIO Y SALAR DE UYUNI (12)
    ("el litio es nuestro",         "frase",   189, "litio",      "alto",  "Reclamo soberano de las comunidades potosinas sobre el litio del Salar de Uyuni",                      date(2026, 1, 7)),
    ("el salar se muere",           "frase",   164, "litio",      "alto",  "Temor a la degradación ambiental del Salar de Uyuni por extracción masiva de salmuera",                date(2026, 1, 10)),
    ("YLB no cumple",               "frase",   148, "litio",      "alto",  "Crítica a Yacimientos de Litio Bolivianos por incumplir metas de producción y compromisos comunitarios",date(2026, 1, 13)),
    ("el contrato con China",       "frase",   178, "litio",      "alto",  "Referencia al acuerdo YLB-CATL/CBC — debatido como concesión excesiva a China o como industrialización",date(2026, 1, 16)),
    ("la evaporación destruye el agua","frase",143,"litio",       "alto",  "Proceso de extracción de litio por evaporación solar como amenaza al acuífero regional",               date(2026, 1, 19)),
    ("el neocolonialismo chino",    "frase",   134, "litio",      "alto",  "Narrativa de que China reemplaza a España como potencia extractivista — muy activa en redes jóvenes",  date(2026, 1, 23)),
    ("la planta de Llipi",          "termino", 112, "litio",      "medio", "Planta piloto de carbonato de litio en el Salar de Uyuni — producción real muy inferior a las metas",  date(2026, 1, 26)),
    ("el triángulo del litio",      "frase",   128, "litio",      "alto",  "Bolivia-Chile-Argentina como zona de mayor litio del mundo — Potosí pide su parte soberana",           date(2026, 1, 29)),
    ("regalías del salar para el salar","frase",156,"litio",      "alto",  "Demanda comunitaria de que las regalías de litio lleguen directamente a las comunidades del Salar",    date(2026, 2, 1)),
    ("el litio nos salva o nos vende","frase", 167, "litio",      "alto",  "Ambigüedad ciudadana frente al litio: salvación soberana o nueva entrega de recursos naturales",       date(2026, 2, 4)),
    ("el acuífero del altiplano",   "termino", 119, "litio",      "alto",  "Sistema de aguas subterráneas del altiplano potosino amenazado por la extracción de salmuera",         date(2026, 2, 7)),
    ("la salmuera como sangre",     "simbolo", 98,  "litio",      "medio", "Metáfora indígena que equipara la salmuera del salar con la sangre de la Pachamama — no tocar",        date(2026, 2, 10)),

    # COMCIPO Y MOVILIZACIÓN CÍVICA (10)
    ("COMCIPO sale a las calles",   "frase",   176, "civismo",    "alto",  "Convocatoria a movilización de COMCIPO — la expresión más temida por todos los gobiernos de turno",   date(2026, 1, 8)),
    ("el pliego cívico",            "termino", 154, "civismo",    "alto",  "Lista formal de demandas de COMCIPO al Estado — documento que puede desencadenar huelgas generales",   date(2026, 1, 11)),
    ("incumplieron todo",           "frase",   187, "civismo",    "alto",  "Síntesis de la relación COMCIPO-Estado: sucesivos gobiernos firman acuerdos y no los ejecutan",       date(2026, 1, 15)),
    ("el aeropuerto prometido",     "frase",   143, "civismo",    "alto",  "Aeropuerto internacional de Potosí — demanda de 2010 que ningún gobierno ha concretado",              date(2026, 1, 18)),
    ("el hospital de 4to nivel",    "frase",   138, "civismo",    "alto",  "Hospital de alta complejidad para Potosí — promesa incumplida que COMCIPO retoma en cada movilización",date(2026, 1, 21)),
    ("Potosí no se rinde",          "frase",   165, "civismo",    "alto",  "Slogan histórico de la resistencia cívica potosina — movilización y orgullo territorial",              date(2026, 1, 24)),
    ("la huelga cívica",            "termino", 129, "civismo",    "alto",  "Instrumento histórico de COMCIPO — paralización total de la ciudad como presión al Estado",           date(2026, 1, 28)),
    ("el Pumari habla por Potosí",  "frase",   118, "civismo",    "medio", "Referencia a Marco Pumari — ex-líder de COMCIPO con proyección política nacional en 2019",            date(2026, 2, 3)),
    ("Potosí financió a Bolivia",   "frase",   134, "civismo",    "alto",  "Narrativa histórica del aporte potosino a la economía boliviana colonial y republicana sin retorno",   date(2026, 2, 6)),
    ("bloqueo en la ruta a Oruro",  "frase",   122, "civismo",    "alto",  "Bloqueo de la carretera principal — acción de presión clásica de COMCIPO y cooperativistas",          date(2026, 2, 9)),

    # AGUA Y MEDIO AMBIENTE (8)
    ("el río Pilcomayo envenena",   "frase",   158, "ambiente",   "alto",  "El río Pilcomayo, uno de los más contaminados de Sudamérica por metales pesados de la minería",        date(2026, 1, 7)),
    ("el drenaje ácido de minas",   "termino", 132, "ambiente",   "alto",  "DAM (Drenaje Ácido de Minas) — proceso de oxidación que genera ácido sulfúrico y libera metales tóxicos",date(2026, 1, 12)),
    ("el agua de Potosí tiene plomo","frase",  145, "ambiente",   "alto",  "Referencia a la contaminación con plomo, arsénico y cadmio del agua de uso doméstico en Potosí",     date(2026, 1, 17)),
    ("el Kari Kari se contamina",   "frase",   118, "ambiente",   "alto",  "Sistema de lagunas coloniales de Potosí afectado por el drenaje de minas — fuente histórica de agua",  date(2026, 1, 22)),
    ("sin agua no hay altiplano",   "frase",   142, "ambiente",   "alto",  "Demanda crítica de comunidades rurales ante la escasez hídrica agravada por minería y cambio climático",date(2026, 1, 27)),
    ("el glaciar retrocede",        "frase",   126, "ambiente",   "alto",  "Retroceso glaciar en la Cordillera Occidental afecta fuentes de agua dulce del altiplano potosino",    date(2026, 2, 1)),
    ("el cerro emponzoña el aire",  "frase",   134, "ambiente",   "alto",  "Contaminación atmosférica por polvo de sílice y arsénico en Potosí ciudad y barrios circundantes",    date(2026, 2, 5)),
    ("el Pillkomayo es un cementerio","frase", 119, "ambiente",   "alto",  "Hipérbole ciudadana sobre el estado de muerte ecológica del río Pilcomayo aguas abajo de Potosí",     date(2026, 2, 9)),

    # IDENTIDAD E HISTORIA (8)
    ("la maldición del cerro",      "frase",   178, "identidad",  "alto",  "Narrativa fatalista-identitaria: Potosí es un lugar eternamente saqueado por poderes externos",        date(2026, 1, 6)),
    ("el ombligo del mundo",        "frase",   167, "identidad",  "alto",  "Referencia histórica: en el siglo XVII Potosí era la ciudad más grande y rica del mundo conocido",    date(2026, 1, 9)),
    ("500 años de saqueo",          "frase",   189, "identidad",  "alto",  "Narrativa que conecta el extractivismo colonial español con el extractivismo contemporáneo del Estado", date(2026, 1, 13)),
    ("la ch'alla al Tío",           "simbolo", 148, "identidad",  "alto",  "Ritual minero de ofrenda al Tío del Cerro — alcohol, coca, cigarros — antes de entrar al socavón",   date(2026, 1, 17)),
    ("somos los más pobres del más rico","frase",156,"identidad", "alto",  "Paradoja potosina: el departamento más generador de riqueza mineral es el más pobre del país",        date(2026, 1, 21)),
    ("la Casa de la Moneda",        "simbolo", 134, "identidad",  "alto",  "Símbolo del esplendor histórico y del extractivismo — donde la plata potosina se acuñaba para el mundo",date(2026, 1, 25)),
    ("el cerro hermoso y maldito",  "frase",   142, "identidad",  "alto",  "Tensión entre orgullo (Sumaj Orcko) y fatalismo (el cerro que mata) como dualidad identitaria",       date(2026, 1, 29)),
    ("potosino hasta los huesos",   "frase",   128, "identidad",  "alto",  "Expresión de arraigo territorial — orgullo potosino como identidad fuerte incluso en la diáspora",    date(2026, 2, 2)),

    # ECONOMÍA Y POBREZA (10)
    ("el zinc de San Cristóbal no queda","frase",143,"economia",  "alto",  "Referencia a que la mina San Cristóbal (Sumitomo) exporta zinc sin beneficios reales para Potosí",    date(2026, 1, 8)),
    ("las regalías son migajas",    "frase",   167, "economia",   "alto",  "Percepción de que el 11% de regalías que recibe Potosí es insuficiente frente a lo que se extrae",   date(2026, 1, 11)),
    ("Potosí el más pobre",         "frase",   178, "economia",   "alto",  "Descripción del ranking de pobreza — Potosí consistentemente el departamento con más pobreza extrema",date(2026, 1, 15)),
    ("el estaño que ya no está",    "frase",   132, "economia",   "alto",  "Referencia al agotamiento de las reservas de estaño que impulsó la economía potosina por décadas",    date(2026, 1, 19)),
    ("el cooperativista sin jubilación","frase",154,"economia",   "alto",  "La ausencia de sistema de previsión social para cooperativistas — vejez sin pensión ni asistencia",   date(2026, 1, 23)),
    ("sin trabajo al cerro",        "frase",   143, "economia",   "alto",  "El cerro como empleador de último recurso para quien no encuentra otra alternativa económica",          date(2026, 1, 27)),
    ("el precio del zinc baja",     "frase",   128, "economia",   "alto",  "Impacto de la fluctuación de precios internacionales del zinc sobre los ingresos de cooperativistas",  date(2026, 2, 1)),
    ("el Banco Minero",             "termino", 112, "economia",   "medio", "Institución financiera para el sector minero — sus condiciones de crédito afectan a cooperativas",      date(2026, 2, 4)),
    ("no hay inversión en Potosí",  "frase",   137, "economia",   "alto",  "Percepción de abandono estatal — infraestructura, tecnología y servicios no llegan al departamento",   date(2026, 2, 7)),
    ("la deuda del cooperativista", "frase",   119, "economia",   "alto",  "Endeudamiento estructural de mineros que adelantan gastos de operación sin garantía de ingresos",     date(2026, 2, 11)),

    # DESCONFIANZA INSTITUCIONAL (10)
    ("el Estado no llega al cerro", "frase",   156, "desconfianza","alto", "Ausencia del Estado en zonas mineras del Cerro Rico — salud, seguridad y justicia inexistentes",       date(2026, 1, 7)),
    ("COMIBOL y la corrupción",     "frase",   143, "desconfianza","alto", "Historial de corrupción en la Corporación Minera de Bolivia — contratos irregulares con cooperativas",  date(2026, 1, 10)),
    ("los contratos del litio son secretos","frase",167,"desconfianza","alto","Denuncias de falta de transparencia en los contratos YLB-CATL y condiciones con empresas chinas",   date(2026, 1, 14)),
    ("la Gobernación no tiene plata","frase",  132, "desconfianza","alto", "Dependencia de Potosí de transferencias del gobierno central — falta de recursos propios permanente",   date(2026, 1, 18)),
    ("nadie fiscaliza las cooperativas","frase",148,"desconfianza","alto", "Ausencia de supervisión del Estado en seguridad, salud y condiciones laborales en cooperativas",        date(2026, 1, 22)),
    ("el INE miente los datos de pobreza","frase",124,"desconfianza","alto","Desconfianza ciudadana en estadísticas del INE — percepción de que la pobreza real es peor",          date(2026, 1, 26)),
    ("la FENCOMIN habla sola",      "frase",   118, "desconfianza","alto", "Cuestionamiento a que la federación cooperativista represente realmente a los mineros de base",          date(2026, 1, 30)),
    ("Sumitomo se va con el zinc",  "frase",   134, "desconfianza","alto", "Percepción de que la mina San Cristóbal (Sumitomo/Japón) repatría utilidades sin retorno local",        date(2026, 2, 3)),
    ("el juez tiene dueño",         "frase",   112, "desconfianza","alto", "Percepción de corrupción judicial en casos de conflictos entre cooperativas y accidentes mineros",       date(2026, 2, 7)),
    ("la autonomía potosina es mentira","frase",126,"desconfianza","alto", "Percepción de que la descentralización no llega a Potosí — el gobierno central decide todo",             date(2026, 2, 11)),
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
    ("Facebook",  "Noticias Potosí — Actualidad y Análisis",     "polarizado",   185000,
     "Megagrupo local de Facebook con la mayor concentración de debate político potosino. Centro de viralización de noticias sobre el cerro, el litio, COMCIPO y conflictos cooperativistas. Alta mezcla de ciudadanía activa, periodistas locales y operadores políticos.", 9),

    ("WhatsApp",  "Cooperativistas FEDECOMIN Potosí",            "silencioso",    45000,
     "Red de comunicación interna entre cooperativas mineras. Muy difícil de monitorear pero decisiva para la movilización del sector. Se difunden precios del mineral, convocatorias a bloqueos y alertas sobre inspecciones. Alta influencia política real.", 9),

    ("TikTok",    "Mineros del Cerro Rico — Vida Real",          "activo",        78000,
     "Creadores de contenido jóvenes que documentan la vida en los socavones. Videos del interior del Cerro Rico, de la palliri, de la ch'alla al Tío. Alto impacto emocional internacional. Canal de denuncia velada de condiciones de trabajo y silicosis.", 8),

    ("Twitter/X", "Periodistas e intelectuales Potosí",          "amplificador",   9500,
     "Red reducida pero altamente influyente. Periodistas del Correo del Sur, académicos de la UATF y activistas con proyección nacional e internacional. Generan agenda mediática que amplifica las demandas de COMCIPO y las alertas sobre el cerro.", 9),

    ("YouTube",   "Canal Potosí Noticias y Correa del Sur",      "amplificador",  28000,
     "Canales locales de noticias con audiencias fieles. Las entrevistas a dirigentes de COMCIPO y cooperativistas en YouTube son referencias citadas en debates de Facebook. Crecimiento acelerado 2024–2026 ante desconfianza en medios nacionales.", 8),

    ("Facebook",  "COMCIPO — Movimiento Cívico Potosí",          "polarizado",    38000,
     "Página oficial y grupos satélite de COMCIPO. Punto de publicación de pliegos cívicos, convocatorias a marchas y comunicados. Alta actividad en períodos de conflicto. Los comentarios reflejan el pulso cívico de Potosí con más fidelidad que ningún otro canal.", 9),

    ("Radio",     "Radio Potosí / Radio Pio XII / Radio Illimani","silencioso",   245000,
     "Medios de mayor penetración en el departamento, especialmente en zonas rurales y mineras del altiplano. Mensajes en castellano, quechua y aymara. Canal decisivo para movilización de comunidades rurales del salar y comunidades mineras alejadas. Históricamente aliada de los movimientos sociales.", 9),

    ("WhatsApp",  "Comunidades del Salar de Uyuni",              "silencioso",    32000,
     "Redes de comunicación de las comunidades originarias circundantes al Salar de Uyuni: Colcha K, Llica, Tahua, San Juan del Rosario. Canal de organización frente a YLB y las empresas de litio. Muy difícil de monitorear pero crítico para anticipar bloqueos al salar.", 9),
]
for plat, nombre, tipo, tam, desc, inf in comunidades:
    db.add(Community(project_id=pid, plataforma=plat, nombre_grupo=nombre,
                     tipo=tipo, tamanio_estimado=tam, descripcion=desc, influencia=inf))

# ── Riesgos ───────────────────────────────────────────────────────────────
riesgos = [
    ("Colapso estructural inminente en zona norte del Cerro Rico — cota 4,400 msnm en riesgo crítico",
     "Geólogos del Ministerio de Minería y expertos de UNESCO advierten que la cota 4,400 msnm del Cerro Rico está en riesgo de colapso súbito. Las cooperativas siguen perforando por encima de esta cota pese a las prohibiciones. Un derrumbe mayor podría sepultar bocaminas activas con centenares de mineros adentro. Riesgo patrimonial, humanitario y político de magnitud histórica.",
     "rojo", 5, date(2026, 2, 15)),

    ("Crisis hídrica aguda en Potosí ciudad — agua contaminada por metales pesados supera límites OMS",
     "Análisis de agua potable en Potosí ciudad muestran concentraciones de plomo, arsénico y cadmio por encima de los límites seguros de la OMS en al menos 4 barrios periféricos. El drenaje ácido de minas del Cerro Rico contamina fuentes históricas. Sin solución en los próximos 60 días, el riesgo de alerta sanitaria internacional es alto.",
     "rojo", 5, date(2026, 2, 12)),

    ("Escalada de violencia entre cooperativas rivales por control de bocaminas en el Cerro Rico",
     "El conflicto entre cooperativas 'Candelaria' y 'Unificada' por acceso a los niveles 14-16 del Cerro Rico ha derivado en uso de dinamita como arma. Dos mineros heridos en la última semana. La FEDECOMIN no puede mediar. El riesgo de muertos y escalada con bloqueo de toda la actividad minera del cerro es alto.",
     "rojo", 4, date(2026, 2, 10)),

    ("COMCIPO anuncia pliego cívico — huelga general en 21 días si no hay respuesta del gobierno",
     "El Comité Cívico Potosinista aprobó en cabildo abierto un nuevo pliego de 12 puntos incluyendo el aeropuerto, el hospital de 4to nivel, más regalías del litio e industrialización en Potosí. Plazo de 21 días al gobierno central. Si no hay respuesta, huelga general que podría paralizar el departamento.",
     "amarillo", 5, date(2026, 2, 8)),

    ("Comunidades del Salar de Uyuni bloquean acceso a la planta piloto de Llipi",
     "Comunidades de Colcha K y Llica bloquearon el camino de acceso a la planta piloto de YLB en Llipi (Salar de Uyuni) exigiendo mayor participación en regalías y empleo local. YLB no puede operar. Si el bloqueo se extiende, el contrato con CATL puede suspenderse por incumplimiento de condiciones de operación.",
     "amarillo", 4, date(2026, 2, 5)),

    ("Denuncias de irregularidades en el contrato YLB-CATL presentadas ante la Asamblea Legislativa",
     "Parlamentarios de la oposición presentaron interpelación formal al Ministerio de Hidrocarburos por las condiciones del contrato YLB-CATL. Las cláusulas de distribución de utilidades (49% Bolivia/51% CATL) y la ausencia de auditorías independientes son los principales cuestionamientos. Si prospera la interpelación, el contrato puede ser suspendido cautelarmente.",
     "amarillo", 4, date(2026, 2, 3)),

    ("Mina San Cristóbal (Sumitomo) reduce producción por caída de precios internacionales del zinc",
     "Los precios internacionales del zinc han caído un 18% en el último trimestre. La mina San Cristóbal (mayor exportador de zinc de Bolivia, controlada por Sumitomo/Japón) analiza reducir su producción en un 25%. Si se concreta, impacto inmediato en exportaciones bolivianas y en ingresos por regalías del departamento de Potosí.",
     "amarillo", 3, date(2026, 2, 1)),

    ("Alerta epidemiológica de silicosis — OMS documenta Potosí como caso crítico mundial",
     "La Organización Mundial de la Salud incluyó a Potosí en un informe especial sobre silicosis como caso crítico global. El Hospital Daniel Bracamonte reporta 3 nuevos casos de silicosis terminal por semana. La cobertura mediática internacional puede presionar al gobierno boliviano a cerrar bocaminas sin compensación, lo que generaría conflicto social severo.",
     "verde", 2, date(2026, 1, 28)),
]
for tema, desc, nivel, vel, fecha in riesgos:
    db.add(Risk(project_id=pid, tema=tema, descripcion=desc,
                nivel=nivel, velocidad_crecimiento=vel,
                fecha_deteccion=fecha, activo=True))

db.commit()
db.close()

print("✓ Monitoreo Digital Potosí 2026 cargado exitosamente.")
print(f"  Proyecto ID:   {pid}")
print(f"  Narrativas:    {len(narrativas)}")
print(f"  Emociones:     {len(emociones)}")
print(f"  Arquetipos:    {len(arquetipos)}")
print(f"  Lenguaje:      {len(lenguaje_data)} términos")
print(f"  Comunidades:   {len(comunidades)}")
print(f"  Riesgos:       {len(riesgos)}")
