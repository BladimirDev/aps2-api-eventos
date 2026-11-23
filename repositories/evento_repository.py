from sqlalchemy.orm import Session
from models.evento import Evento
from models.inscricao import Inscricao

def criar(db: Session, evento):
    novo_evento = Evento(**evento.model_dump())

    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)
    return novo_evento

def listar(db: Session):
    return db.query(Evento).all()

def buscar_por_id(db: Session, evento_id):
    return db.query(Evento).filter(
        Evento.id == evento_id
    ).first()

def atualizar(db: Session, evento_id, evento_atualizado):
    evento = buscar_por_id(db, evento_id)
    if evento is None:
        return None

    dados = evento_atualizado.model_dump()
    for campo, valor in dados.items():
        setattr(evento, campo, valor)
    db.commit()
    db.refresh(evento)
    return evento

def excluir(db: Session, evento_id):
    evento = buscar_por_id(db, evento_id)
    if evento is None:
        return None

    db.delete(evento)
    db.commit()
    return evento

def tem_inscricoes(db: Session, evento_id):
    return db.query(Inscricao).filter(
        Inscricao.evento_id == evento_id
    ).first() is not None
