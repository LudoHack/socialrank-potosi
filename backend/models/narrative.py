from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Narrative(Base):
    __tablename__ = "narratives"

    id               = Column(Integer, primary_key=True, index=True)
    project_id       = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    texto            = Column(Text, nullable=False)
    tipo             = Column(String(50))   # dominante | emergente | contrarrelato
    actor_politico   = Column(String(200))
    fecha_deteccion  = Column(Date)
    peso             = Column(Float, default=5.0)  # 1-10
    created_at       = Column(DateTime(timezone=True), server_default=func.now())
