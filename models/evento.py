from pydantic import BaseModel, Field
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