# API de Eventos Acadêmicos — APS 3

Projeto desenvolvido para a Avaliação Parcial 03 da disciplina de Desenvolvimento Back-End. A aplicação dá continuidade à API da APS 2, substituindo o armazenamento em memória por persistência em banco SQLite com SQLAlchemy ORM e acrescentando relatórios de consolidação.

## Objetivo

Gerenciar eventos acadêmicos, participantes e inscrições, mantendo os dados salvos após o encerramento da aplicação. A API também disponibiliza relatórios calculados a partir dos registros existentes no banco.

## Tecnologias

- Python
- FastAPI
- SQLite
- SQLAlchemy ORM
- Pydantic
- Uvicorn
- Swagger / OpenAPI

## Requisitos

- Python 3.10 ou superior;
- `pip` para instalar as dependências.

## Como executar

1. Abra o terminal na pasta `aps2-api-eventos`.
2. (Recomendado) Crie e ative um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

   Windows (PowerShell):

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Linux / macOS:

   ```bash
   source .venv/bin/activate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Inicie a API:

   ```bash
   uvicorn main:app --reload
   ```

5. Acesse a documentação interativa:

    - Swagger: http://127.0.0.1:8000/docs
    - OpenAPI: http://127.0.0.1:8000/openapi.json
    - Rota inicial: http://127.0.0.1:8000/

Na primeira inicialização, as tabelas são criadas automaticamente a partir dos modelos SQLAlchemy registrados em `main.py`.

## Banco de dados

O projeto utiliza SQLite. A conexão está configurada em `database.py` com o endereço `sqlite:///./eventos.db`. Portanto, o arquivo `eventos.db` é criado na pasta de execução do projeto (normalmente a própria pasta `aps2-api-eventos`).

O arquivo do banco é local e está incluído no `.gitignore` para evitar o envio acidental de dados de execução ao repositório. Ao clonar o projeto em outro computador, a aplicação cria um banco novo na primeira execução. Os dados permanecem salvos entre reinicializações enquanto o arquivo `eventos.db` for mantido.

## Funcionalidades e rotas

### Eventos

| Método | Rota | Descrição |
|---|---|---|
| POST | `/eventos` | Cadastrar evento |
| GET | `/eventos` | Listar eventos |
| GET | `/eventos/{evento_id}` | Consultar evento pelo ID |
| PUT | `/eventos/{evento_id}` | Atualizar evento |
| DELETE | `/eventos/{evento_id}` | Excluir evento, se não possuir inscrições |

Exemplo de corpo para `POST /eventos`:

```json
{
  "titulo": "Palestra de Tecnologia",
  "descricao": "Evento sobre desenvolvimento de software",
  "data": "2026-12-15",
  "horario": "19:00:00",
  "local": "UniSenai",
  "capacidade": 50,
  "categoria": "Tecnologia"
}
```

### Participantes

| Método | Rota | Descrição |
|---|---|---|
| POST | `/participantes` | Cadastrar participante |
| GET | `/participantes` | Listar participantes |
| GET | `/participantes/{participante_id}` | Consultar participante pelo ID |
| PUT | `/participantes/{participante_id}` | Atualizar participante |
| DELETE | `/participantes/{participante_id}` | Excluir participante, se não possuir inscrições |

Exemplo de corpo para `POST /participantes`:

```json
{
  "nome": "Joao Silva",
  "email": "joao@email.com",
  "curso": "Engenharia de Software"
}
```

### Inscrições

| Método | Rota | Descrição |
|---|---|---|
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Inscrever participante em evento |
| GET | `/eventos/{evento_id}/inscricoes` | Listar inscrições de um evento |

A criação da inscrição verifica se o evento e o participante existem, se a inscrição já foi realizada e se ainda há vagas. A combinação de `evento_id` e `participante_id` também possui restrição de unicidade no banco.

### Relatórios

| Método | Rota | Informações retornadas |
|---|---|---|
| GET | `/relatorios/ocupacao-eventos` | Capacidade, inscritos, vagas disponíveis e percentual de ocupação por evento |
| GET | `/relatorios/eventos-por-categoria` | Quantidade de eventos, capacidade total e inscrições por categoria |
| GET | `/relatorios/participacao-por-curso` | Quantidade de participantes distintos e inscrições por curso |

Os relatórios são calculados dinamicamente com consultas SQLAlchemy. O relatório de ocupação inclui eventos sem inscrições; o relatório por curso conta participantes distintos para não contar a mesma pessoa mais de uma vez.

## Validações e tratamento de erros

A API utiliza Pydantic para validar os dados recebidos. Entre as regras implementadas estão:

- Título do evento e nome do participante não podem ser vazios;
- Capacidade do evento deve ser maior que zero;
- Data e horário devem possuir formatos válidos;
- E-mail deve possuir formato válido e ser único;
- Um participante não pode ter duas inscrições no mesmo evento;
- Não é permitido exceder a capacidade do evento;
- Não é permitida a exclusão de evento ou participante que possua inscrições relacionadas.

Principais respostas HTTP:

- `201 Created`: cadastro ou inscrição realizada;
- `200 OK`: consulta ou atualização realizada;
- `204 No Content`: exclusão realizada;
- `404 Not Found`: evento ou participante não encontrado;
- `409 Conflict`: e-mail duplicado, inscrição duplicada, evento sem vagas ou tentativa de excluir registro com inscrições;
- `422 Unprocessable Entity`: dados enviados não passaram pela validação.

## Organização do projeto

```text
aps2-api-eventos/
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── eventos.db                 # criado localmente ao executar a aplicação
├── controllers/
│   ├── evento_controller.py
│   ├── participante_controller.py
│   ├── inscricao_controller.py
│   └── relatorio_controller.py
├── models/
│   ├── evento.py
│   ├── participante.py
│   └── inscricao.py
├── schemas/
│   ├── evento_schema.py
│   ├── participante_schema.py
│   └── inscricao_schema.py
├── services/
│   ├── evento_service.py
│   ├── participante_service.py
│   ├── inscricao_service.py
│   └── relatorio_service.py
└── repositories/
    ├── evento_repository.py
    ├── participante_repository.py
    ├── inscricao_repository.py
    └── relatorio_repository.py
```

### Responsabilidade das camadas

- **Controllers:** definem as rotas HTTP, recebem parâmetros e retornam respostas;
- **Schemas:** validam os dados de entrada e definem os formatos de resposta com Pydantic;
- **Models:** representam as tabelas e os relacionamentos no SQLAlchemy;
- **Services:** aplicam as regras de negócio;
- **Repositories:** realizam consultas e operações no banco de dados;
- **Database:** configura a conexão, a sessão e a disponibilização do acesso ao SQLite.

## Roteiro de testes pelo Swagger

Com a API em execução, abra `/docs` e teste os seguintes cenários:

1. Cadastrar e consultar um evento;
2. Cadastrar e consultar um participante;
3. Atualizar evento e participante;
4. Criar uma inscrição válida;
5. Tentar repetir a mesma inscrição e verificar `409`;
6. Tentar inscrever participante ou evento inexistente e verificar `404`;
7. Criar evento com capacidade 1, realizar uma inscrição e tentar uma segunda para verificar `409`;
8. Tentar cadastrar outro participante com o mesmo e-mail e verificar `409`;
9. Tentar excluir evento ou participante com inscrições e verificar `409`;
10. Reiniciar a aplicação e consultar novamente os registros para verificar a persistência;
11. Consultar os três relatórios;
12. Inserir ou alterar registros e consultar os relatórios novamente para verificar a atualização dos resultados.

Os testes podem ser realizados diretamente pelo Swagger, que permite visualizar os corpos das requisições, as respostas JSON e os códigos HTTP.