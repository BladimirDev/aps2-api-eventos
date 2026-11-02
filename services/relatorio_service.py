from repositories import relatorio_repository

def ocupacao_eventos(db):
    return relatorio_repository.ocupacao_eventos(db)

def eventos_por_categoria(db):
    return relatorio_repository.eventos_por_categoria(db)

def participacao_por_curso(db):
    return relatorio_repository.participacao_por_curso(db)