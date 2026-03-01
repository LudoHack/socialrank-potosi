from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Emotion(Base):
    __tablename__ = "emotions"

    id          = Column(Integer, primary_key=True, index=True)
    project_id  = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    tipo        = Column(String(50), nullable=False)  # ira|miedo|frustracion|esperanza|desconfianza|orgullo
    intensidad  = Column(Float, default=5.0)          # 1-10
    fuente      = Column(String(200))
    fecha       = Column(Date)
    notas       = Column(Text)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
