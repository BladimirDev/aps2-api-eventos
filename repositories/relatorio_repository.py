from sqlalchemy.orm import Session
from sqlalchemy import func
from models.evento import Evento
from models.participante import Participante
from models.inscricao import Inscricao

def ocupacao_eventos(db: Session):
    total_inscricoes = func.count(Inscricao.id)
    resultados = db.query(
        Evento.id,
        Evento.titulo,
        Evento.capacidade,
        total_inscricoes.label("total_inscritos")
    ).outerjoin(
        Inscricao,
        Evento.id == Inscricao.evento_id).group_by(Evento.id
    ).all()
    relatorio = []

    for evento in resultados:
        vagas_disponiveis = evento.capacidade - evento.total_inscritos

        percentual = (evento.total_inscritos / evento.capacidade) * 100

        relatorio.append({
            "evento_id": evento.id,
            "titulo": evento.titulo,
            "capacidade": evento.capacidade,
            "total_inscritos": evento.total_inscritos,
            "vagas_disponiveis": vagas_disponiveis,
            "percentual_ocupacao": round(percentual, 2)
        })
    return relatorio

def eventos_por_categoria(db: Session):

    inscricoes_por_evento = db.query(
        Inscricao.evento_id.label("evento_id"),
        func.count(Inscricao.id).label("total_inscricoes")
    ).group_by(
        Inscricao.evento_id
    ).subquery()

    resultados = db.query(
        Evento.categoria,
        func.count(Evento.id).label("total_eventos"),
        func.sum(Evento.capacidade).label("capacidade_total"),
        func.coalesce(
            func.sum(inscricoes_por_evento.c.total_inscricoes),
            0
        ).label("total_inscricoes")
    ).outerjoin(
        inscricoes_por_evento,
        Evento.id == inscricoes_por_evento.c.evento_id
    ).group_by(
        Evento.categoria
    ).all()

    relatorio = []

    for categoria in resultados:
        relatorio.append({
            "categoria": categoria.categoria,
            "total_eventos": categoria.total_eventos,
            "capacidade_total": categoria.capacidade_total,
            "total_inscricoes": categoria.total_inscricoes
        })
    return relatorio

def participacao_por_curso(db: Session):

    resultados = db.query(
        Participante.curso,
        func.count(
            func.distinct(Participante.id)
        ).label("total_participantes"),
        func.count(Inscricao.id).label("total_inscricoes")
    ).outerjoin(
        Inscricao,
        Participante.id == Inscricao.participante_id
    ).group_by(
        Participante.curso
    ).all()

    relatorio = []

    for curso in resultados:
        relatorio.append({
            "curso": curso.curso,
            "total_participantes": curso.total_participantes,
            "total_inscricoes": curso.total_inscricoes
        })
    return relatorio