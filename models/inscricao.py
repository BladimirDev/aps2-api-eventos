from datetime import date
from sqlalchemy import ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Inscricao(Base):
    __tablename__ = "inscricoes"
    __table_args__= (UniqueConstraint("evento_id", "participante_id",name="uq_evento_participante"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    evento_id: Mapped[int] = mapped_column(ForeignKey("eventos.id"), nullable=False)
    participante_id: Mapped[int] = mapped_column(ForeignKey("participantes.id"), nullable=False)
    data_inscricao: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)

    evento = relationship("Evento", back_populates="inscricoes")
    participante = relationship("Participante", back_populates="inscricoes")