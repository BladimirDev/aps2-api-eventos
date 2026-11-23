from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import date, time
from typing import Optional


class EventoCreate(BaseModel):
    titulo: str = Field(min_length=1)
    descricao: str
    data: date
    horario: time
    local: str
    capacidade: int = Field(gt=0)
    categoria: str

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor):
        if not valor.strip():
            raise ValueError("O título do evento não pode estar vazio.")
        return valor.strip()

class EventoResponse(EventoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)