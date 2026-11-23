from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from controllers import evento_controller
from controllers import participante_controller
from controllers import inscricao_controller
from controllers import relatorio_controller
from controllers import usuario_controller
from controllers import auth_controller
from models import evento, inscricao, participante, usuario
from database import Base, engine, SessionLocal
from services import usuario_service

Base.metadata.create_all(bind=engine)

# cria o administrador inicial (dados vindos do .env), caso ainda não exista
db = SessionLocal()
try:
    usuario_service.criar_admin_inicial(db)
finally:
    db.close()

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API RESTful para gerenciamento de eventos acadêmicos, participantes e inscrições.",
    version="2.0.0"
)

app.include_router(auth_controller.router)
app.include_router(usuario_controller.router)
app.include_router(evento_controller.router)
app.include_router(participante_controller.router)
app.include_router(inscricao_controller.router)
app.include_router(relatorio_controller.router)

@app.exception_handler(SQLAlchemyError)
def erro_banco_de_dados(request: Request, erro: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocorreu um erro ao acessar o banco de dados. Tente novamente."}
    )

@app.get("/")
def inicio():
    return {
        "mensagem": "API de Eventos Acadêmicos funcionando!"
    }