from repositories import inscricao_repository
from repositories import evento_repository
from repositories import participante_repository

class EventoNaoEncontradoError(Exception):
    pass

class ParticipanteNaoEncontradoError(Exception):
    pass

class ParticipanteJaInscritoError(Exception):
    pass

class SemVagasError(Exception):
    pass

def criar_inscricao(db, evento_id, participante_id):
    evento = evento_repository.buscar_por_id(db, evento_id)
    if evento is None:
        raise EventoNaoEncontradoError("Evento não encontrado.")

    participante = participante_repository.buscar_por_id(db,participante_id)
    if participante is None:
        raise ParticipanteNaoEncontradoError("Participante não encontrado.")

    inscricao_existente = inscricao_repository.buscar(db,evento_id,participante_id)

    if inscricao_existente is not None:
        raise ParticipanteJaInscritoError("Participante já está inscrito neste evento.")

    total_inscricoes = inscricao_repository.contar_por_evento(db,evento_id)

    if total_inscricoes >= evento.capacidade:
        raise SemVagasError("Não existem vagas disponíveis para este evento.")

    return inscricao_repository.criar(db,evento_id,participante_id)

def listar_inscricoes(db, evento_id):
    evento = evento_repository.buscar_por_id(db, evento_id)
    if evento is None:
        raise EventoNaoEncontradoError("Evento não encontrado.")

    return inscricao_repository.listar_por_evento(db,evento_id)