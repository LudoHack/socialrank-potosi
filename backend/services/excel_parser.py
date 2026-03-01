import pandas as pd
import tempfile, os
from sqlalchemy.orm import Session
from models.narrative import Narrative
from models.emotion import Emotion
from models.archetype import Archetype
from models.language_code import LanguageCode
from models.community import Community
from models.risk import Risk

def _safe_date(val):
    try:
        if pd.isna(val): return None
        return pd.to_datetime(val).date()
    except:
        return None

def _safe_float(val, default=5.0):
    try:
        if pd.isna(val): return default
        return float(val)
    except:
        return default

def _safe_int(val, default=0):
    try:
        if pd.isna(val): return default
        return int(val)
    except:
        return default

def _safe_str(val):
    if pd.isna(val): return None
    return str(val).strip() or None

def _parse_narrativas(df: pd.DataFrame, project_id: int, db: Session) -> int:
    count = 0
    for _, row in df.iterrows():
        texto = _safe_str(row.get("texto"))
        if not texto: continue
        db.add(Narrative(
            project_id=project_id,
            texto=texto,
            tipo=_safe_str(row.get("tipo")) or "dominante",
            actor_politico=_safe_str(row.get("actor")),
            fecha_deteccion=_safe_date(row.get("fecha")),
            peso=_safe_float(row.get("peso"), 5.0),
        ))
        count += 1
    return count

def _parse_emociones(df: pd.DataFrame, project_id: int, db: Session) -> int:
    count = 0
    for _, row in df.iterrows():
        tipo = _safe_str(row.get("tipo"))
        if not tipo: continue
        db.add(Emotion(
            project_id=project_id,
            tipo=tipo.lower(),
            intensidad=_safe_float(row.get("intensidad"), 5.0),
            fuente=_safe_str(row.get("fuente")),
            fecha=_safe_date(row.get("fecha")),
            notas=_safe_str(row.get("notas")),
        ))
        count += 1
    return count

def _parse_arquetipos(df: pd.DataFrame, project_id: int, db: Session) -> int:
    count = 0
    for _, row in df.iterrows():
        nombre = _safe_str(row.get("nombre"))
        if not nombre: continue
        canales_raw = _safe_str(row.get("canales"))
        canales = [c.strip() for c in canales_raw.split(",")] if canales_raw else []
        db.add(Archetype(
            project_id=project_id,
            nombre=nombre,
            descripcion=_safe_str(row.get("descripcion")),
            peso_relativo=_safe_float(row.get("peso_relativo"), 0.0),
            emocion_dominante=_safe_str(row.get("emocion")),
            canales=canales,
            valores_clave=_safe_str(row.get("valores_clave")),
            miedos=_safe_str(row.get("miedos")),
        ))
        count += 1
    return count

def _parse_lenguaje(df: pd.DataFrame, project_id: int, db: Session) -> int:
    count = 0
    for _, row in df.iterrows():
        termino = _safe_str(row.get("termino"))
        if not termino: continue
        db.add(LanguageCode(
            project_id=project_id,
            termino=termino,
            tipo=_safe_str(row.get("tipo")) or "frase",
            frecuencia=_safe_int(row.get("frecuencia"), 1),
            contexto=_safe_str(row.get("contexto")),
            fecha_deteccion=_safe_date(row.get("fecha")),
        ))
        count += 1
    return count

def _parse_comunidades(df: pd.DataFrame, project_id: int, db: Session) -> int:
    count = 0
    for _, row in df.iterrows():
        nombre = _safe_str(row.get("nombre"))
        if not nombre: continue
        db.add(Community(
            project_id=project_id,
            plataforma=_safe_str(row.get("plataforma")),
            nombre_grupo=nombre,
            tipo=_safe_str(row.get("tipo")) or "activo",
            tamanio_estimado=_safe_int(row.get("tamanio")),
            descripcion=_safe_str(row.get("descripcion")),
            influencia=_safe_int(row.get("influencia"), 5),
        ))
        count += 1
    return count

def _parse_riesgos(df: pd.DataFrame, project_id: int, db: Session) -> int:
    count = 0
    for _, row in df.iterrows():
        tema = _safe_str(row.get("tema"))
        if not tema: continue
        db.add(Risk(
            project_id=project_id,
            tema=tema,
            descripcion=_safe_str(row.get("descripcion")),
            nivel=_safe_str(row.get("nivel")) or "amarillo",
            velocidad_crecimiento=_safe_int(row.get("velocidad"), 3),
            fecha_deteccion=_safe_date(row.get("fecha")),
            activo=True,
        ))
        count += 1
    return count

SHEET_MAP = {
    "narrativas":  _parse_narrativas,
    "emociones":   _parse_emociones,
    "arquetipos":  _parse_arquetipos,
    "lenguaje":    _parse_lenguaje,
    "comunidades": _parse_comunidades,
    "riesgos":     _parse_riesgos,
}

def parse_excel(path: str, project_id: int, db: Session) -> dict:
    xl = pd.ExcelFile(path)
    importados = {}
    for sheet in xl.sheet_names:
        key = sheet.lower().strip()
        if key in SHEET_MAP:
            df = xl.parse(sheet)
            df.columns = [str(c).lower().strip() for c in df.columns]
            count = SHEET_MAP[key](df, project_id, db)
            importados[key] = count
    db.commit()
    return importados

def generate_template() -> str:
    path = tempfile.mktemp(suffix=".xlsx")
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        sheets = {
            "narrativas":  ["texto", "tipo", "actor", "fecha", "peso"],
            "emociones":   ["tipo", "intensidad", "fuente", "fecha", "notas"],
            "arquetipos":  ["nombre", "descripcion", "peso_relativo", "emocion", "canales", "valores_clave", "miedos"],
            "lenguaje":    ["termino", "tipo", "frecuencia", "contexto", "fecha"],
            "comunidades": ["plataforma", "nombre", "tipo", "tamanio", "descripcion", "influencia"],
            "riesgos":     ["tema", "descripcion", "nivel", "velocidad", "fecha"],
        }
        hints = {
            "narrativas":  [["El desempleo es culpa del gobierno", "dominante", "Candidato A", "2024-03-15", 8]],
            "emociones":   [["ira", 7, "Twitter", "2024-03-15", "Comentarios en posts políticos"]],
            "arquetipos":  [["El desencantado", "Votante de 35-50 años que perdió confianza", 25, "frustración", "WhatsApp,Radio", "Estabilidad,Familia", "Desempleo,Inseguridad"]],
            "lenguaje":    [["la gente decente", "frase", 45, "Discurso del candidato A", "2024-03-10"]],
            "comunidades": [["Facebook", "Padres por la educación", "amplificador", 12000, "Grupo activo de padres", 8]],
            "riesgos":     [["Escándalo de corrupción emergente", "Filtraciones en prensa", "rojo", 4, "2024-03-20"]],
        }
        wb = writer.book
        header_fmt = wb.add_format({"bold": True, "bg_color": "#1a1d27", "font_color": "#7c6af7", "border": 1})
        hint_fmt = wb.add_format({"italic": True, "font_color": "#7b82a8"})
        for sheet_name, cols in sheets.items():
            df = pd.DataFrame(columns=cols)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            ws = writer.sheets[sheet_name]
            for col_idx, col in enumerate(cols):
                ws.write(0, col_idx, col, header_fmt)
                ws.set_column(col_idx, col_idx, max(len(col) + 5, 18))
            for row_idx, row_data in enumerate(hints.get(sheet_name, [])):
                for col_idx, val in enumerate(row_data):
                    ws.write(row_idx + 1, col_idx, val, hint_fmt)
    return path
