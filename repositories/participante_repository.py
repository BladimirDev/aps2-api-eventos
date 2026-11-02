from sqlalchemy.orm import Session
from models.participante import Participante
from models.inscricao import Inscricao

def criar(db: Session, participante):
    novo_participante = Participante(**participante.model_dump())

    db.add(novo_participante)
    db.commit()
    db.refresh(novo_participante)

    return novo_participante

def listar(db: Session):
    return db.query(Participante).all()

def buscar_por_id(db: Session, participante_id):
    return db.query(Participante).filter(
        Participante.id == participante_id
    ).first()

def atualizar(db: Session, participante_id, participante_atualizado):
    participante = buscar_por_id(db, participante_id)
    if participante is None:
        return None

    dados = participante_atualizado.model_dump()
    for campo, valor in dados.items():
        setattr(participante, campo, valor)
    db.commit()
    db.refresh(participante)
    return participante

def excluir(db: Session, participante_id):
    participante = buscar_por_id(db, participante_id)
    if participante is None:
        return None

    db.delete(participante)
    db.commit()
    return participante

def tem_inscricoes(db: Session, participante_id):
    return db.query(Inscricao).filter(Inscricao.participante_id == participante_id).first() is not None


def buscar_por_email(db: Session, email):
    return db.query(Participante).filter(Participante.email == email).first()