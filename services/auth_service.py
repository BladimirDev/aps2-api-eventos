from repositories import usuario_repository
from security.security import verificar_senha, criar_token


class CredenciaisInvalidasError(Exception):
    pass


def login(db, email, senha):
    usuario = usuario_repository.buscar_por_email(db, email)

    # a mesma mensagem para e-mail inexistente e senha errada,
    # assim ninguém descobre quais e-mails estão cadastrados
    if usuario is None or not verificar_senha(senha, usuario.senha_hash):
        raise CredenciaisInvalidasError("E-mail ou senha inválidos.")

    token = criar_token(usuario.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
