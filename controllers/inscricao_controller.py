from fastapi import APIRouter, HTTPException, status
from services import inscricao_service

router = APIRouter(
    prefix="/eventos",
    tags=["Inscrições"]
)

@router.post(
    "/{evento_id}/inscricoes/{participante_id}",
    status_code=status.HTTP_201_CREATED
)
def criar_inscricao(evento_id: int, participante_id: int):

    try:
        return inscricao_service.criar_inscricao(
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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )
    except inscricao_service.SemVagasError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro)
        )

@router.get("/{evento_id}/inscricoes")
def listar_inscricoes(evento_id: int):

    try:
        return inscricao_service.listar_inscricoes(
            evento_id
        )
    except inscricao_service.EventoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(erro)
        )