from fastapi import FastAPI
from controllers import evento_controller
from controllers import participante_controller
from controllers import inscricao_controller

app = FastAPI(
    title="API de Eventos Acadêmicos",
    description="API RESTful para gerenciamento de eventos acadêmicos, participantes e inscrições.",
    version="1.0.0"
)

app.include_router(evento_controller.router)
app.include_router(participante_controller.router)
app.include_router(inscricao_controller.router)

@app.get("/")
def inicio():
    return {
        "mensagem": "API de Eventos Acadêmicos funcionando!"
    }