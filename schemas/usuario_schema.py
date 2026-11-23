from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict


class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr

    # o bcrypt só considera até 72 bytes, por isso o limite máximo
    senha: str = Field(min_length=6, max_length=72)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor):
        if not valor.strip():
            raise ValueError("O nome do usuário não pode estar vazio.")
        return valor.strip()

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor):
        if not valor.strip():
            raise ValueError("A senha não pode ser formada apenas por espaços.")
        return valor


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    perfil: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
