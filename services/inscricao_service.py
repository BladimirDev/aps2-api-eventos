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

def criar_inscricao(evento_id, participante_id):
    # Verifica se o evento existe
    evento = evento_repository.buscar_por_id(evento_id)

    if evento is None:
        raise EventoNaoEncontradoError(
            "Evento não encontrado."
        )

    # Verifica se o participante existe
    participante = participante_repository.buscar_por_id(
        participante_id
    )

    if participante is None:
        raise ParticipanteNaoEncontradoError(
            "Participante não encontrado."
        )

    # Verifica se o participante já está inscrito
    inscricao_existente = inscricao_repository.buscar(
        evento_id,
        participante_id
    )

    if inscricao_existente is not None:
        raise ParticipanteJaInscritoError(
            "Participante já está inscrito neste evento."
        )

    # Para verificar a quantidade de inscrições
    inscricoes = inscricao_repository.listar_por_evento(
        evento_id
    )

    # Aqui verifica se ainda existem vagas
    if len(inscricoes) >= evento.capacidade:
        raise SemVagasError(
            "Não existem vagas disponíveis para este evento."
        )

    # Aqui é pra criar a inscrição
    return inscricao_repository.criar(
        evento_id,
        participante_id
    )

def listar_inscricoes(evento_id):
    # Verifica se o evento existe
    evento = evento_repository.buscar_por_id(evento_id)

    if evento is None:
        raise EventoNaoEncontradoError(
            "Evento não encontrado."
        )
    return inscricao_repository.listar_por_evento(
        evento_id
    )