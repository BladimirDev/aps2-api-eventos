from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    # a senha original nunca é salva, só o hash gerado pelo bcrypt
    senha_hash: Mapped[str] = mapped_column(String, nullable=False)

    perfil: Mapped[str] = mapped_column(String, nullable=False, default="usuario")
