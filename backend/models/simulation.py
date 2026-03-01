from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from database import Base

class Simulation(Base):
    __tablename__ = "simulations"

    id                  = Column(Integer, primary_key=True, index=True)
    project_id          = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    mensaje_propuesto   = Column(Text, nullable=False)
    resultado_json      = Column(JSON)   # respuesta estructurada de Claude
    created_at          = Column(DateTime(timezone=True), server_default=func.now())
