from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional


class Evento(BaseModel):
    id: Optional[int] = None

    titulo: str = Field(min_length=1)
    descricao: str
    data: date
    horario: str
    local: str
    capacidade: int = Field(gt=0)
    categoria: str

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor):
        if not valor.strip():
            raise ValueError("O título do evento não pode estar vazio.")
        return valor.strip()