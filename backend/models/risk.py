from sqlalchemy import Column, Integer, String, Text, Date, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

class Risk(Base):
    __tablename__ = "risks"

    id                      = Column(Integer, primary_key=True, index=True)
    project_id              = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    tema                    = Column(String(300), nullable=False)
    descripcion             = Column(Text)
    nivel                   = Column(String(20), default="amarillo")  # verde|amarillo|rojo
    velocidad_crecimiento   = Column(Integer, default=3)  # 1-5
    narrativas_relacionadas = Column(JSON, default=list)  # list of narrative ids
    fecha_deteccion         = Column(Date)
    activo                  = Column(Boolean, default=True)
    created_at              = Column(DateTime(timezone=True), server_default=func.now())
