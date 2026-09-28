from fastapi import APIRouter, HTTPException, status
from models.evento import Evento
from services import evento_service

router = APIRouter(
    prefix="/eventos",
    tags=["Eventos"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_evento(evento: Evento):
    return evento_service.criar(evento)

@router.get("/")
def listar_eventos():
    return evento_service.listar()

@router.get("/{evento_id}")
def buscar_evento(evento_id: int):
    evento = evento_service.buscar_por_id(evento_id)

    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )
    return evento

@router.put("/{evento_id}")
def atualizar_evento(evento_id: int, evento: Evento):
    evento_atualizado = evento_service.atualizar(
        evento_id,
        evento
    )
    if evento_atualizado is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )
    return evento_atualizado

@router.delete(
    "/{evento_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_evento(evento_id: int):
    evento_excluido = evento_service.excluir(evento_id)

    if evento_excluido is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento não encontrado."
        )
    return None