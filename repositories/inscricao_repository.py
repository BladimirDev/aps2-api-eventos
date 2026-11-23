from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from models.inscricao import Inscricao

def criar(db: Session, evento_id, participante_id):
    inscricao = Inscricao(evento_id=evento_id,participante_id=participante_id)

    db.add(inscricao)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(inscricao)
    return inscricao

def listar_por_evento(db: Session, evento_id):
    return db.query(Inscricao).options(joinedload(Inscricao.participante)).filter(Inscricao.evento_id == evento_id).all()

def buscar(db: Session, evento_id, participante_id):
    return db.query(Inscricao).filter(Inscricao.evento_id == evento_id,Inscricao.participante_id == participante_id).first()

def contar_por_evento(db: Session, evento_id):
    return db.query(Inscricao).filter(Inscricao.evento_id == evento_id).count()