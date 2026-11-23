participantes = []
proximo_id = 1

def criar(participante):
    global proximo_id

    participante.id = proximo_id
    proximo_id += 1

    participantes.append(participante)

    return participante

def listar():
    return participantes

def buscar_por_id(participante_id):
    for participante in participantes:
        if participante.id == participante_id:
            return participante

    return None

def atualizar(participante_id, participante_atualizado):
    for i, participante in enumerate(participantes):
        if participante.id == participante_id:
            participante_atualizado.id = participante_id
            participantes[i] = participante_atualizado

            return participante_atualizado

    return None

def excluir(participante_id):
    for i, participante in enumerate(participantes):
        if participante.id == participante_id:
            return participantes.pop(i)

    return None