from repositories import evento_repository

def criar(evento):
    return evento_repository.criar(evento)

def listar():
    return evento_repository.listar()

def buscar_por_id(evento_id):
    evento = evento_repository.buscar_por_id(evento_id)

    if evento is None:
        return None

    return evento

def atualizar(evento_id, evento_atualizado):
    evento = evento_repository.buscar_por_id(evento_id)

    if evento is None:
        return None

    return evento_repository.atualizar(
        evento_id,
        evento_atualizado
    )

def excluir(evento_id):
    evento = evento_repository.buscar_por_id(evento_id)

    if evento is None:
        return None

    return evento_repository.excluir(evento_id)