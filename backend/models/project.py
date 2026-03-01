from sqlalchemy import Column, Integer, String, Boolean, Date, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id              = Column(Integer, primary_key=True, index=True)
    nombre          = Column(String(200), nullable=False)
    cliente         = Column(String(200))
    contexto_pais   = Column(String(100))
    fecha_inicio    = Column(Date)
    descripcion     = Column(Text)
    activo          = Column(Boolean, default=True)
    created_at      = Column(DateTime(timezone=True), server_default=func.now())
    updated_at      = Column(DateTime(timezone=True), onupdate=func.now())
