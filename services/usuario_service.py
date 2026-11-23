import os
from sqlalchemy.exc import IntegrityError
from repositories import usuario_repository
from security.security import gerar_hash_senha


class EmailJaCadastradoError(Exception):
    pass


def criar(db, usuario):
    usuario_existente = usuario_repository.buscar_por_email(db, usuario.email)

    if usuario_existente is not None:
        raise EmailJaCadastradoError(
            "Já existe um usuário cadastrado com este e-mail."
        )

    senha_hash = gerar_hash_senha(usuario.senha)

    # todo cadastro feito pela rota pública vira "usuario",
    # mesmo que alguém tente mandar "perfil": "administrador" no corpo
    try:
        return usuario_repository.criar(
            db,
            usuario.nome,
            usuario.email,
            senha_hash,
            "usuario"
        )
    except IntegrityError:
        raise EmailJaCadastradoError(
            "Já existe um usuário cadastrado com este e-mail."
        )


def criar_admin_inicial(db):
    # o administrador inicial é criado a partir das variáveis do .env
    nome = os.getenv("ADMIN_NOME", "Administrador")
    email = os.getenv("ADMIN_EMAIL")
    senha = os.getenv("ADMIN_SENHA")

    if not email or not senha:
        return

    if usuario_repository.buscar_por_email(db, email) is not None:
        return

    usuario_repository.criar(
        db,
        nome,
        email,
        gerar_hash_senha(senha),
        "administrador"
    )
