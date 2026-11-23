from sqlalchemy import String, Integer, Date, Time
from datetime import date, time
from sqlalchemy.orm import Mapped, mapped_column, relationship, MappedSQLExpression
from database import Base

class Evento(Base):
    __tablename__ = "eventos"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String, nullable=False)
    descricao: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    horario: Mapped[time] = mapped_column(Time, nullable=False)
    local: Mapped[str] = mapped_column(String, nullable=False)
    capacidade: Mapped[int] = mapped_column(Integer, nullable=False)
    categoria: Mapped[str] = mapped_column(String, nullable=False)

    inscricoes = relationship("Inscricao", back_populates="evento")