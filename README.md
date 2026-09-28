# API de Eventos Acadêmicos

Este projeto foi desenvolvido para a Avaliação Parcial 02 da disciplina de Desenvolvimento Back-End.

A proposta é criar uma API RESTful para ajudar uma instituição de ensino a organizar seus eventos acadêmicos, como palestras, workshops, minicursos, seminários e competições.

A API permite cadastrar eventos e participantes, além de realizar e consultar inscrições.

## Objetivo do projeto

O principal objetivo foi colocar em prática os conteúdos estudados durante a disciplina, principalmente:

- Python
- FastAPI
- Pydantic
- APIs RESTful
- JSON
- Métodos HTTP
- Validação de dados
- Tratamento de erros
- Arquitetura MVC e separação em camadas

## O que a API faz?

Com a API é possível:

- Cadastrar um evento;
- Listar os eventos cadastrados;
- Consultar um evento pelo ID;
- Atualizar um evento;
- Excluir um evento;
- Cadastrar participantes;
- Listar os participantes;
- Consultar um participante pelo ID;
- Atualizar um participante;
- Excluir um participante;
- Inscrever um participante em um evento;
- Consultar os participantes inscritos em um evento.

Além disso, a API verifica algumas regras, como:

- O evento precisa existir para receber uma inscrição;
- O participante precisa estar cadastrado;
- O mesmo participante não pode se inscrever duas vezes no mesmo evento;
- O evento não pode ultrapassar sua capacidade.

## Tecnologias utilizadas

- Python
- FastAPI
- Pydantic
- Uvicorn
- JSON
- Swagger

## Organização do projeto

O projeto foi separado em algumas pastas para deixar o código mais organizado:

```text
aps2-api-eventos/
│
├── main.py
├── requirements.txt
├── README.md
│
├── controllers/
│   ├── __init__.py
│   ├── evento_controller.py
│   ├── participante_controller.py
│   └── inscricao_controller.py
│
├── models/
│   ├── __init__.py
│   ├── evento.py
│   └── participante.py
│
├── services/
│   ├── __init__.py
│   ├── evento_service.py
│   ├── participante_service.py
│   └── inscricao_service.py
│
└── repositories/
    ├── __init__.py
    ├── evento_repository.py
    ├── participante_repository.py
    └── inscricao_repository.py
