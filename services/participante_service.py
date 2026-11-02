from repositories import participante_repository

class EmailDuplicadoError(Exception):
    pass

class ParticipanteComInscricoesError(Exception):
    pass

def criar(db, participante):
    participante_existente = participante_repository.buscar_por_email(db,participante.email)

    if participante_existente is not None:
        raise EmailDuplicadoError(
            "Já existe um participante cadastrado com este e-mail."
        )
    return participante_repository.criar(db, participante)

def listar(db):
    return participante_repository.listar(db)

def buscar_por_id(db, participante_id):
    return participante_repository.buscar_por_id(
        db,
        participante_id
    )

def atualizar(db, participante_id, participante_atualizado):
    participante = participante_repository.buscar_por_id(
        db,
        participante_id
    )

    if participante is None:
        return None

    participante_existente = participante_repository.buscar_por_email(
        db,
        participante_atualizado.email
    )

    if participante_existente is not None and participante_existente.id != participante_id:
        raise EmailDuplicadoError(
            "Já existe um participante cadastrado com este e-mail."
        )
    return participante_repository.atualizar(db, participante_id,participante_atualizado)

def excluir(db, participante_id):
    participante = participante_repository.buscar_por_id(db,participante_id)
    if participante is None:
        return None

    if participante_repository.tem_inscricoes(db, participante_id):
        raise ParticipanteComInscricoesError(
            "Não é possível excluir um participante que possui inscrições."
        )
    return participante_repository.excluir(db, participante_id)