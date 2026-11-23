from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.usuario import Usuario


def criar(db: Session, nome, email, senha_hash, perfil):
    novo_usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        perfil=perfil
    )

    db.add(novo_usuario)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(novo_usuario)

    return novo_usuario

def buscar_por_id(db: Session, usuario_id):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def buscar_por_email(db: Session, email):
    return db.query(Usuario).filter(Usuario.email == email).first()
