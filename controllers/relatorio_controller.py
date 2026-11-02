from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services import relatorio_service

router = APIRouter(
    prefix="/relatorios",
    tags=["Relatórios"]
)

@router.get("/ocupacao-eventos")
def ocupacao_eventos(db: Session = Depends(get_db)):
    return relatorio_service.ocupacao_eventos(db)

@router.get("/eventos-por-categoria")
def eventos_por_categoria(db: Session = Depends(get_db)):
    return relatorio_service.eventos_por_categoria(db)

@router.get("/participacao-por-curso")
def participacao_por_curso(db: Session = Depends(get_db)):
    return relatorio_service.participacao_por_curso(db)
