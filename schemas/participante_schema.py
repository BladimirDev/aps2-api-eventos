from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from typing import Optional


class ParticipanteCreate(BaseModel):
    nome: str
    email: EmailStr
    curso: str

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if not valor.strip():
            raise ValueError("O nome do participante não pode estar vazio.")
        return valor.strip()

class ParticipanteResponse(ParticipanteCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)