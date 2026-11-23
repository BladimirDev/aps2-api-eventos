from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario_schema import LoginRequest, TokenResponse, UsuarioResponse
from services import auth_service
from security.security import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

@router.post("/login", response_model=TokenResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    try:
        return auth_service.login(db, dados.email, dados.senha)

    except auth_service.CredenciaisInvalidasError as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(erro)
        )

@router.get("/me", response_model=UsuarioResponse)
def usuario_logado(usuario=Depends(get_current_user)):
    return usuario
