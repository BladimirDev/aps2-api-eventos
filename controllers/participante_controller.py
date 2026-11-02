from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.participante_schema import (ParticipanteCreate,ParticipanteResponse)
from services import participante_service

router = APIRouter(
    prefix="/participantes",
    tags=["Participantes"]
)

@router.post("",response_model=ParticipanteResponse,status_code=status.HTTP_201_CREATED)
def criar_participante(participante: ParticipanteCreate,db: Session = Depends(get_db)):
    try:
        return participante_service.criar(db, participante)

    except participante_service.EmailDuplicadoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )

@router.get("", response_model=list[ParticipanteResponse])
def listar_participantes(db: Session = Depends(get_db)):
    return participante_service.listar(db)

@router.get("/{participante_id}", response_model=ParticipanteResponse)
def buscar_participante(participante_id: int,db: Session = Depends(get_db)):
    participante = participante_service.buscar_por_id(db,participante_id)

    if participante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )
    return participante

@router.put("/{participante_id}", response_model=ParticipanteResponse)
def atualizar_participante(participante_id: int,participante: ParticipanteCreate,db: Session = Depends(get_db)):
    try:
        participante_atualizado = participante_service.atualizar(
            db,
            participante_id,
            participante
        )
        if participante_atualizado is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante não encontrado."
            )
        return participante_atualizado

    except participante_service.EmailDuplicadoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )

@router.delete("/{participante_id}",status_code=status.HTTP_204_NO_CONTENT)
def excluir_participante(participante_id: int,db: Session = Depends(get_db)):
    try:
        participante_excluido = participante_service.excluir(
            db,
            participante_id
        )
        if participante_excluido is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participante não encontrado."
            )
        return None
    except participante_service.ParticipanteComInscricoesError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )