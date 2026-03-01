from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class LanguageCode(Base):
    __tablename__ = "language_codes"

    id               = Column(Integer, primary_key=True, index=True)
    project_id       = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    termino          = Column(String(300), nullable=False)
    tipo             = Column(String(50))   # frase|apodo|meme|simbolo|ironico
    frecuencia       = Column(Integer, default=1)
    contexto         = Column(Text)
    fecha_deteccion      = Column(Date)
    funcion_cultural     = Column(String(50))   # indecision|desconfianza|activacion|espanto|economia|gestion|emocional|identidad
    impacto_voto_blando  = Column(String(20))   # activa|neutral|espanta
    created_at           = Column(DateTime(timezone=True), server_default=func.now())
