from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.inscricao_schema import InscricaoResponse, InscricaoComParticipanteResponse
from services import inscricao_service
from security.security import get_current_user, verificar_admin

router = APIRouter(prefix="/eventos",tags=["Inscrições"])

@router.post("/{evento_id}/inscricoes/{participante_id}",response_model=InscricaoResponse,status_code=status.HTTP_201_CREATED)
def criar_inscricao(evento_id: int,participante_id: int,db: Session = Depends(get_db), usuario=Depends(get_current_user)):
    try:
        return inscricao_service.criar_inscricao(
            db,
            evento_id,
            participante_id
        )

    except inscricao_service.EventoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro)
        )

    except inscricao_service.ParticipanteNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro)
        )

    except inscricao_service.ParticipanteJaInscritoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )

    except inscricao_service.SemVagasError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro)
        )

@router.get("/{evento_id}/inscricoes",response_model=list[InscricaoComParticipanteResponse])
def listar_inscricoes(evento_id: int,db: Session = Depends(get_db), admin=Depends(verificar_admin)):
    try:
        return inscricao_service.listar_inscricoes(
            db,
            evento_id
        )

    except inscricao_service.EventoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro)
        )