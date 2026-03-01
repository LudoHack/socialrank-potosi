import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import create_tables
from routes import projects, upload, dashboard, narratives, emotions, archetypes, language, communities, risks, ai, evolution, ivb

app = FastAPI(title="Social Rank Bolivia — Potosí API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()
    # Auto-seed si la BD está vacía
    try:
        from database import SessionLocal
        from models.project import Project
        db = SessionLocal()
        count = db.query(Project).count()
        db.close()
        if count == 0:
            import seed_potosi
    except Exception as e:
        print(f"[seed] Error: {e}")

# ── API routes ────────────────────────────────────────────────────────────
app.include_router(projects.router,     prefix="/api/projects",     tags=["Proyectos"])
app.include_router(upload.router,       prefix="/api/upload",        tags=["Upload"])
app.include_router(dashboard.router,    prefix="/api/dashboard",     tags=["Dashboard"])
app.include_router(narratives.router,   prefix="/api/narratives",    tags=["Narrativas"])
app.include_router(emotions.router,     prefix="/api/emotions",      tags=["Emociones"])
app.include_router(archetypes.router,   prefix="/api/archetypes",    tags=["Arquetipos"])
app.include_router(language.router,     prefix="/api/language",      tags=["Lenguaje"])
app.include_router(communities.router,  prefix="/api/communities",   tags=["Comunidades"])
app.include_router(risks.router,        prefix="/api/risks",         tags=["Riesgos"])
app.include_router(ai.router,           prefix="/api/ai",            tags=["IA"])
app.include_router(evolution.router,    prefix="/api/evolution",     tags=["Evolución"])
app.include_router(ivb.router,          prefix="/api/ivb",           tags=["IVB"])

# ── Servir frontend React (build estático) ────────────────────────────────
_DIST = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")

if os.path.isdir(_DIST):
    # Archivos estáticos de Vite (/assets/*, *.ico, *.svg, etc.)
    app.mount("/assets", StaticFiles(directory=os.path.join(_DIST, "assets")), name="assets")

    # SPA fallback: cualquier ruta que no sea /api → index.html
    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        return FileResponse(os.path.join(_DIST, "index.html"))
else:
    @app.get("/")
    def root():
        return {"status": "ok", "app": "EtnoDB API — frontend no compilado"}
