inscricoes = []

def criar(evento_id, participante_id):
    inscricao = {
        "evento_id": evento_id,
        "participante_id": participante_id
    }

    inscricoes.append(inscricao)

    return inscricao

def listar_por_evento(evento_id):
    return [
        inscricao
        for inscricao in inscricoes
        if inscricao["evento_id"] == evento_id
    ]

def buscar(evento_id, participante_id):
    for inscricao in inscricoes:
        if (
            inscricao["evento_id"] == evento_id
            and inscricao["participante_id"] == participante_id
        ):
            return inscricao

    return None