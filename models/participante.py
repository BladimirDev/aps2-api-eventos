from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Participante(Base):
    __tablename__ = "participantes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    curso: Mapped[str] = mapped_column(String, nullable=False)

    inscricoes = relationship("Inscricao", back_populates="participante")