from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.evento_schema import EventoCreate, EventoResponse
from services import evento_service

router = APIRouter(
    prefix="/eventos",
    tags=["Eventos"]
)

@router.post("",response_model=EventoResponse,status_code=status.HTTP_201_CREATED)
def criar_evento(evento: EventoCreate, db: Session = Depends(get_db)):
    return evento_service.criar(db, evento)

@router.get("", response_model=list[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar(db)

@router.get("/{evento_id}", response_model=EventoResponse)
def buscar_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = evento_service.buscar_por_id(db, evento_id)
    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )
    return evento

@router.put("/{evento_id}", response_model=EventoResponse)
def atualizar_evento(evento_id: int,evento: EventoCreate,db: Session = Depends(get_db)):
    evento_atualizado = evento_service.atualizar(
        db,
        evento_id,
        evento
    )
    if evento_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )
    return evento_atualizado

@router.delete("/{evento_id}",status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(evento_id: int, db: Session = Depends(get_db)):
    try:
        evento_excluido = evento_service.excluir(db, evento_id)
        if evento_excluido is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Evento não encontrado."
            )
        return None
    except evento_service.EventoComInscricoesError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )