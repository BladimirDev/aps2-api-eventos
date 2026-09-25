from pydantic import BaseModel, EmailStr
from typing import Optional


class Participante(BaseModel):
    id: Optional[int] = None

    nome: str
    email: EmailStr
    curso: str