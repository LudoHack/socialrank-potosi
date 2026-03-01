from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Community(Base):
    __tablename__ = "communities"

    id               = Column(Integer, primary_key=True, index=True)
    project_id       = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    plataforma       = Column(String(100))   # Twitter|Facebook|WhatsApp|TikTok|Radio|etc.
    nombre_grupo     = Column(String(300))
    tipo             = Column(String(50))    # activo|polarizado|amplificador|silencioso
    tamanio_estimado = Column(Integer)
    descripcion      = Column(Text)
    influencia       = Column(Integer, default=5)  # 1-10
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
