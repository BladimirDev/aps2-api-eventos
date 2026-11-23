from fastapi import APIRouter, HTTPException, status
from models.participante import Participante
from services import participante_service

router = APIRouter(
    prefix="/participantes",
    tags=["Participantes"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_participante(participante: Participante):
    return participante_service.criar(participante)

@router.get("")
def listar_participantes():
    return participante_service.listar()

@router.get("/{participante_id}")
def buscar_participante(participante_id: int):
    participante = participante_service.buscar_por_id(participante_id)

    if participante is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )
    return participante

@router.put("/{participante_id}")
def atualizar_participante(
    participante_id: int,
    participante: Participante
):
    participante_atualizado = participante_service.atualizar(
        participante_id,
        participante
    )

    if participante_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )
    return participante_atualizado

@router.delete(
    "/{participante_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_participante(participante_id: int):
    participante_excluido = participante_service.excluir(
        participante_id
    )

    if participante_excluido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participante não encontrado."
        )
    return None