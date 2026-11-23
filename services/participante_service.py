from repositories import participante_repository

def criar(participante):
    return participante_repository.criar(participante)

def listar():
    return participante_repository.listar()

def buscar_por_id(participante_id):
    participante = participante_repository.buscar_por_id(participante_id)

    if participante is None:
        return None

    return participante

def atualizar(participante_id, participante_atualizado):
    participante = participante_repository.buscar_por_id(participante_id)

    if participante is None:
        return None

    return participante_repository.atualizar(
        participante_id,
        participante_atualizado
    )

def excluir(participante_id):
    participante = participante_repository.buscar_por_id(participante_id)

    if participante is None:
        return None

    return participante_repository.excluir(participante_id)