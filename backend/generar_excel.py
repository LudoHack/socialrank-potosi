"""
Genera el Excel santa_cruz_2026.xlsx con todos los datos del proyecto.
Ejecutar: python generar_excel.py
"""
import pandas as pd

output = "D:/etnografica/backend/santa_cruz_2026.xlsx"

# ── NARRATIVAS ────────────────────────────────────────────────────────────────
narrativas = pd.DataFrame([
    {"texto": "La ciudad está abandonada, nadie gobierna de verdad",    "tipo": "dominante",     "actor": "Ciudadanos urbanos",             "fecha": "2026-05-12", "peso": 9},
    {"texto": "Todo sube menos el salario, ya no alcanza",               "tipo": "dominante",     "actor": "Trabajadores y comerciantes",    "fecha": "2026-05-14", "peso": 8},
    {"texto": "Necesitamos orden y seguridad, no discursos",             "tipo": "dominante",     "actor": "Vecinos y juntas barriales",     "fecha": "2026-05-16", "peso": 8},
    {"texto": "Todos prometen, pero nadie cumple",                       "tipo": "dominante",     "actor": "Opinión pública general",        "fecha": "2026-05-18", "peso": 9},
    {"texto": "Todavía no hay por quién decidirse",                      "tipo": "dominante",     "actor": "Electores indecisos",            "fecha": "2026-05-19", "peso": 9},
    {"texto": "Todos tienen algo malo",                                  "tipo": "dominante",     "actor": "Opinión pública general",        "fecha": "2026-05-20", "peso": 8},
    {"texto": "Este candidato al menos escucha a la gente",              "tipo": "emergente",     "actor": "Seguidores del candidato",       "fecha": "2026-05-20", "peso": 6},
    {"texto": "La crisis viene del gobierno central, no del municipio",  "tipo": "emergente",     "actor": "Analistas y medios locales",     "fecha": "2026-05-22", "peso": 5},
    {"texto": "Puede definirlo cualquier error",                         "tipo": "emergente",     "actor": "Analistas locales",              "fecha": "2026-05-22", "peso": 7},
    {"texto": "Es más de lo mismo, viene de la misma élite",             "tipo": "contrarrelato", "actor": "Opositores internos",            "fecha": "2026-05-23", "peso": 6},
    {"texto": "Santa Cruz necesita alguien firme, no improvisado",       "tipo": "contrarrelato", "actor": "Grupos conservadores",           "fecha": "2026-05-25", "peso": 7},
])

# ── EMOCIONES ─────────────────────────────────────────────────────────────────
emociones = pd.DataFrame([
    {"tipo": "frustracion",  "intensidad": 8, "fuente": "Facebook",    "fecha": "2026-05-12", "notas": "Quejas por precios altos y falta de empleo"},
    {"tipo": "ira",          "intensidad": 7, "fuente": "Twitter/X",   "fecha": "2026-05-13", "notas": "Ataques contra autoridades actuales"},
    {"tipo": "desconfianza", "intensidad": 9, "fuente": "Bigdata",        "fecha": "2026-05-14", "notas": "Rechazo general a políticos tradicionales"},
    {"tipo": "miedo",        "intensidad": 6, "fuente": "WhatsApp",       "fecha": "2026-05-15", "notas": "Inseguridad y robos en barrios"},
    {"tipo": "frustracion",  "intensidad": 7, "fuente": "Escucha Social", "fecha": "2026-05-16", "notas": "Sensación de estancamiento económico"},
    {"tipo": "esperanza",    "intensidad": 5, "fuente": "Facebook",    "fecha": "2026-05-17", "notas": "Expectativa moderada ante nuevo candidato"},
    {"tipo": "ira",          "intensidad": 8, "fuente": "Twitter/X",   "fecha": "2026-05-18", "notas": "Debate por crisis de dólar"},
    {"tipo": "desconfianza", "intensidad": 8, "fuente": "Entrevistas", "fecha": "2026-05-19", "notas": "Dudas sobre promesas electorales"},
    {"tipo": "desconfianza", "intensidad": 9, "fuente": "Bigdata",        "fecha": "2026-05-20", "notas": "No identificación clara con ningún candidato"},
    {"tipo": "miedo",        "intensidad": 7, "fuente": "Radio",          "fecha": "2026-05-20", "notas": "Discusión sobre violencia urbana"},
    {"tipo": "esperanza",    "intensidad": 6, "fuente": "Facebook",       "fecha": "2026-05-21", "notas": "Propuestas concretas de empleo"},
    {"tipo": "frustracion",  "intensidad": 7, "fuente": "Escucha Social", "fecha": "2026-05-21", "notas": "Cansancio ante opciones poco convincentes"},
    {"tipo": "frustracion",  "intensidad": 6, "fuente": "Bigdata",        "fecha": "2026-05-22", "notas": "Cansancio con peleas políticas"},
    {"tipo": "esperanza",    "intensidad": 4, "fuente": "Facebook",    "fecha": "2026-05-22", "notas": "Expectativa débil de sorpresa posible"},
    {"tipo": "miedo",        "intensidad": 5, "fuente": "WhatsApp",    "fecha": "2026-05-23", "notas": "Temor a equivocarse al elegir"},
    {"tipo": "orgullo",      "intensidad": 5, "fuente": "Boca a boca", "fecha": "2026-05-23", "notas": "Identidad cruceña y autosuperación"},
])

# ── ARQUETIPOS ────────────────────────────────────────────────────────────────
arquetipos = pd.DataFrame([
    {
        "nombre": "El votante blando expectante",
        "descripcion": "Adultos urbanos y clase media que comparan opciones, consumen información pero evitan definirse públicamente",
        "peso_relativo": 32,
        "emocion": "desconfianza",
        "canales": "Facebook,YouTube,Prensa,WhatsApp",
        "valores_clave": "cautela, racionalidad, estabilidad",
        "miedos": "equivocarse, decepción, manipulación",
    },
    {
        "nombre": "El trabajador frustrado",
        "descripcion": "Adultos de sectores populares y medios bajos, empleo inestable y alto costo de vida",
        "peso_relativo": 25,
        "emocion": "frustracion",
        "canales": "Facebook,WhatsApp,Radio",
        "valores_clave": "trabajo, estabilidad, esfuerzo, familia",
        "miedos": "desempleo, inflación, abandono",
    },
    {
        "nombre": "El indignado activo",
        "descripcion": "Usuarios politizados, muy vocales y críticos del sistema",
        "peso_relativo": 18,
        "emocion": "ira",
        "canales": "Twitter/X,Facebook,TikTok",
        "valores_clave": "justicia, castigo, verdad",
        "miedos": "corrupción, impunidad",
    },
    {
        "nombre": "El pragmático silencioso",
        "descripcion": "Clase media ocupada, observa más de lo que comenta",
        "peso_relativo": 14,
        "emocion": "desconfianza",
        "canales": "Facebook,YouTube,Prensa",
        "valores_clave": "orden, resultados, previsibilidad",
        "miedos": "improvisación, caos",
    },
    {
        "nombre": "El esperanzado moderado",
        "descripcion": "Jóvenes y adultos que buscan alternativas nuevas",
        "peso_relativo": 7,
        "emocion": "esperanza",
        "canales": "Instagram,TikTok,YouTube",
        "valores_clave": "cambio, oportunidades, diálogo",
        "miedos": "repetir el pasado, falta de futuro",
    },
    {
        "nombre": "El nostálgico del orden",
        "descripcion": "Adultos mayores y conservadores urbanos",
        "peso_relativo": 4,
        "emocion": "miedo",
        "canales": "TV,Radio,Boca a boca",
        "valores_clave": "autoridad, respeto, seguridad",
        "miedos": "delincuencia, descontrol",
    },
])

# ── LENGUAJE ──────────────────────────────────────────────────────────────────
# funcion_cultural: indecision | desconfianza | activacion | espanto | economia | gestion | identidad
# impacto_voto_blando: activa | neutral | espanta
lenguaje = pd.DataFrame([
    # 🔵 Indecisión / Voto Blando
    {"termino": "Todavía estoy viendo",    "tipo": "frase",   "frecuencia": 214, "contexto": "Indecisión explícita previa a la elección",          "fecha": "2026-05-20", "funcion_cultural": "indecision",   "impacto_voto_blando": "activa"},
    {"termino": "No me convence ninguno",  "tipo": "frase",   "frecuencia": 198, "contexto": "Rechazo general sin polarización",                   "fecha": "2026-05-21", "funcion_cultural": "indecision",   "impacto_voto_blando": "activa"},
    {"termino": "Capaz a último momento",  "tipo": "frase",   "frecuencia":  97, "contexto": "Decisión postergada hasta el final",                 "fecha": "2026-05-26", "funcion_cultural": "indecision",   "impacto_voto_blando": "activa"},
    {"termino": "Depende qué pase",        "tipo": "frase",   "frecuencia":  84, "contexto": "Voto condicional a eventos futuros",                 "fecha": "2026-05-22", "funcion_cultural": "indecision",   "impacto_voto_blando": "activa"},
    # 🟡 Desconfianza suave
    {"termino": "Más de lo mismo",         "tipo": "ironico", "frecuencia": 187, "contexto": "Deslegitimación suave de candidatos tradicionales",  "fecha": "2026-05-23", "funcion_cultural": "desconfianza", "impacto_voto_blando": "neutral"},
    {"termino": "Ver para creer",          "tipo": "frase",   "frecuencia": 129, "contexto": "Exigencia de pruebas antes de apoyar",               "fecha": "2026-05-23", "funcion_cultural": "desconfianza", "impacto_voto_blando": "neutral"},
    {"termino": "Puro discurso",           "tipo": "frase",   "frecuencia": 154, "contexto": "Rechazo a promesas vacías",                          "fecha": "2026-05-16", "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta"},
    {"termino": "Habla bonito, pero…",     "tipo": "ironico", "frecuencia":  76, "contexto": "Duda sobre credibilidad del candidato",               "fecha": "2026-05-27", "funcion_cultural": "desconfianza", "impacto_voto_blando": "neutral"},
    {"termino": "Político de siempre",     "tipo": "apodo",   "frecuencia": 121, "contexto": "Etiqueta negativa para candidatos tradicionales",    "fecha": "2026-05-17", "funcion_cultural": "desconfianza", "impacto_voto_blando": "espanta"},
    # 🟢 Activación potencial
    {"termino": "Por lo menos habla claro","tipo": "frase",   "frecuencia": 162, "contexto": "Evaluación positiva moderada, puerta de entrada",    "fecha": "2026-05-22", "funcion_cultural": "activacion",   "impacto_voto_blando": "activa"},
    {"termino": "Con hechos, no palabras", "tipo": "frase",   "frecuencia": 171, "contexto": "Demanda de acciones concretas antes de votar",       "fecha": "2026-05-25", "funcion_cultural": "activacion",   "impacto_voto_blando": "activa"},
    {"termino": "Eso sí es concreto",      "tipo": "frase",   "frecuencia": 112, "contexto": "Activación potencial del voto blando",               "fecha": "2026-05-26", "funcion_cultural": "activacion",   "impacto_voto_blando": "activa"},
    {"termino": "Trabajar sin show",       "tipo": "frase",   "frecuencia":  96, "contexto": "Rechazo a la política espectáculo",                  "fecha": "2026-05-24", "funcion_cultural": "activacion",   "impacto_voto_blando": "activa"},
    # 🔴 Espanto del voto blando
    {"termino": "Mano dura total",         "tipo": "simbolo", "frecuencia":  84, "contexto": "Discurso que genera rechazo en el voto blando",      "fecha": "2026-05-25", "funcion_cultural": "espanto",      "impacto_voto_blando": "espanta"},
    {"termino": "Que se vayan todos",      "tipo": "frase",   "frecuencia":  87, "contexto": "Expresión de voto castigo generalizado",             "fecha": "2026-05-19", "funcion_cultural": "espanto",      "impacto_voto_blando": "espanta"},
    {"termino": "Sin peleas políticas",    "tipo": "frase",   "frecuencia":  88, "contexto": "Cansancio ante la polarización, quiebre del elector","fecha": "2026-05-27", "funcion_cultural": "espanto",      "impacto_voto_blando": "espanta"},
    # 🟪 Economía cotidiana
    {"termino": "No alcanza",              "tipo": "frase",   "frecuencia": 342, "contexto": "Queja recurrente sobre economía familiar",           "fecha": "2026-05-12", "funcion_cultural": "economia",     "impacto_voto_blando": "activa"},
    {"termino": "Meme del bolsillo vacío", "tipo": "meme",    "frecuencia":  98, "contexto": "Humor gráfico sobre crisis económica",               "fecha": "2026-05-18", "funcion_cultural": "economia",     "impacto_voto_blando": "activa"},
    {"termino": "Prometer no cuesta nada", "tipo": "ironico", "frecuencia": 109, "contexto": "Sarcasmo político sobre compromisos económicos",     "fecha": "2026-05-21", "funcion_cultural": "economia",     "impacto_voto_blando": "neutral"},
    # 🟫 Gestión y vida diaria
    {"termino": "Ciudad abandonada",       "tipo": "frase",   "frecuencia": 215, "contexto": "Crítica a la gestión municipal",                     "fecha": "2026-05-13", "funcion_cultural": "gestion",      "impacto_voto_blando": "espanta"},
    {"termino": "Ordenar la casa",         "tipo": "simbolo", "frecuencia": 118, "contexto": "Metáfora de gestión eficiente y pragmática",         "fecha": "2026-05-24", "funcion_cultural": "gestion",      "impacto_voto_blando": "activa"},
    {"termino": "Lo básico primero",       "tipo": "simbolo", "frecuencia": 134, "contexto": "Prioridad de gestión pragmática y municipal",        "fecha": "2026-05-28", "funcion_cultural": "gestion",      "impacto_voto_blando": "activa"},
    # 🟦 Identidad local
    {"termino": "Santa Cruz primero",      "tipo": "simbolo", "frecuencia": 133, "contexto": "Orgullo e identidad local, no ideológica",           "fecha": "2026-05-20", "funcion_cultural": "identidad",    "impacto_voto_blando": "neutral"},
    {"termino": "Trabajo honesto",         "tipo": "frase",   "frecuencia":  72, "contexto": "Valor cultural identitario cruceño",                 "fecha": "2026-05-22", "funcion_cultural": "identidad",    "impacto_voto_blando": "neutral"},
])

# ── COMUNIDADES ───────────────────────────────────────────────────────────────
comunidades = pd.DataFrame([
    {"plataforma": "TikTok",      "nombre": "SCZ en Corto",             "tipo": "amplificador", "tamanio": 92000, "descripcion": "Videos virales de crítica social",                         "influencia": 9},
    {"plataforma": "Facebook",    "nombre": "Vecinos Unidos SCZ",       "tipo": "activo",       "tamanio": 48000, "descripcion": "Grupo barrial con alto debate sobre seguridad y servicios",  "influencia": 8},
    {"plataforma": "Radio",       "nombre": "Radio Popular 104.5",      "tipo": "amplificador", "tamanio": 65000, "descripcion": "Agenda temas de inseguridad y economía",                   "influencia": 8},
    {"plataforma": "Boca a boca", "nombre": "Mercados y ferias",        "tipo": "activo",       "tamanio": 50000, "descripcion": "Conversación directa y altamente influyente",              "influencia": 7},
    {"plataforma": "Twitter/X",   "nombre": "Opinión Cruceña",          "tipo": "polarizado",   "tamanio": 15000, "descripcion": "Discusión política intensa y confrontativa",                "influencia": 7},
    {"plataforma": "WhatsApp",    "nombre": "Comerciantes Centro SCZ",  "tipo": "silencioso",   "tamanio":   320, "descripcion": "Difusión de quejas económicas y rumores",                   "influencia": 6},
])

# ── RIESGOS ───────────────────────────────────────────────────────────────────
riesgos = pd.DataFrame([
    {"tema": "Voto castigo generalizado",               "descripcion": "Rechazo transversal a todos los candidatos",                                  "nivel": "rojo",     "velocidad": 5, "fecha": "2026-05-18"},
    {"tema": "Migración del voto blando a abstención",  "descripcion": "Falta de activación emocional puede llevar a no votar",                       "nivel": "rojo",     "velocidad": 4, "fecha": "2026-05-23"},
    {"tema": "Crisis económica local",                  "descripcion": "Conversación creciente sobre precios y desempleo",                            "nivel": "amarillo", "velocidad": 4, "fecha": "2026-05-16"},
    {"tema": "Desinformación en WhatsApp",              "descripcion": "Circulación de audios y cadenas falsas",                                      "nivel": "amarillo", "velocidad": 3, "fecha": "2026-05-20"},
    {"tema": "Ataques al candidato por pasado político","descripcion": "Narrativa que busca asociarlo a la élite",                                    "nivel": "amarillo", "velocidad": 3, "fecha": "2026-05-22"},
    {"tema": "Baja participación juvenil",              "descripcion": "Desinterés electoral temprano",                                               "nivel": "verde",    "velocidad": 2, "fecha": "2026-05-23"},
])

# ── GENERAR EXCEL ─────────────────────────────────────────────────────────────
sheets = {
    "narrativas":  narrativas,
    "emociones":   emociones,
    "arquetipos":  arquetipos,
    "lenguaje":    lenguaje,
    "comunidades": comunidades,
    "riesgos":     riesgos,
}

with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
    wb = writer.book
    header_fmt  = wb.add_format({"bold": True, "bg_color": "#1a1d27", "font_color": "#7c6af7", "border": 1})
    text_fmt    = wb.add_format({"text_wrap": True, "valign": "top"})

    for name, df in sheets.items():
        df.to_excel(writer, sheet_name=name, index=False)
        ws = writer.sheets[name]
        ws.set_row(0, 18)
        for col_idx, col in enumerate(df.columns):
            ws.write(0, col_idx, col, header_fmt)
            max_w = max(len(col) + 4, df[col].astype(str).str.len().max() + 3)
            ws.set_column(col_idx, col_idx, min(max_w, 65), text_fmt)

print(f"Archivo generado: {output}")
print()
for name, df in sheets.items():
    print(f"  {name:15s}: {len(df):2d} filas")
