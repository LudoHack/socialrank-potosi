from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

class Archetype(Base):
    __tablename__ = "archetypes"

    id               = Column(Integer, primary_key=True, index=True)
    project_id       = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    nombre           = Column(String(200), nullable=False)
    descripcion      = Column(Text)
    peso_relativo    = Column(Float, default=0.0)   # % del electorado / audiencia
    emocion_dominante = Column(String(50))
    canales          = Column(JSON, default=list)   # ["Twitter","Radio","WhatsApp"]
    valores_clave    = Column(Text)
    miedos           = Column(Text)
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
