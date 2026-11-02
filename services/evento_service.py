from repositories import evento_repository

class EventoComInscricoesError(Exception):
    pass

def criar(db, evento):
    return evento_repository.criar(db, evento)

def listar(db):
    return evento_repository.listar(db)

def buscar_por_id(db, evento_id):
    return evento_repository.buscar_por_id(db, evento_id)

def atualizar(db, evento_id, evento_atualizado):
    return evento_repository.atualizar(db,evento_id,evento_atualizado)

def excluir(db, evento_id):
    evento = evento_repository.buscar_por_id(db, evento_id)
    if evento is None:
        return None

    if evento_repository.tem_inscricoes(db, evento_id):
        raise EventoComInscricoesError(
            "Não é possível excluir um evento que possui inscrições."
        )
    return evento_repository.excluir(db, evento_id)