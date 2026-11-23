eventos = []
proximo_id = 1

def criar(evento):
    global proximo_id

    evento.id = proximo_id
    proximo_id += 1
    eventos.append(evento)

    return evento

def listar():
    return eventos

def buscar_por_id(evento_id):
    for evento in eventos:
        if evento.id == evento_id:
            return evento

    return None

def atualizar(evento_id, evento_atualizado):
    for i, evento in enumerate(eventos):
        if evento.id == evento_id:
            evento_atualizado.id = evento_id
            eventos[i] = evento_atualizado

            return evento_atualizado
    return None

def excluir(evento_id):
    for i, evento in enumerate(eventos):
        if evento.id == evento_id:

            return eventos.pop(i)
    return None