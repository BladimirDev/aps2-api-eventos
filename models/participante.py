from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


class Participante(BaseModel):
    id: Optional[int] = None

    nome: str
    email: EmailStr
    curso: str

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if not valor.strip():
            raise ValueError("O nome do participante não pode estar vazio.")
        return valor.strip()