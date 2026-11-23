# API de Eventos Acadêmicos — APS 4

Projeto desenvolvido para a Avaliação Parcial 04 da disciplina de Desenvolvimento Back-End. A aplicação dá continuidade à API da APS 3 (eventos, participantes, inscrições e relatórios com SQLite e SQLAlchemy) e acrescenta **autenticação e segurança**: cadastro de usuários, senhas armazenadas como hash, login com token JWT, proteção das rotas e controle de acesso por perfil.

## Objetivo

Gerenciar eventos acadêmicos, participantes e inscrições, mantendo os dados salvos no banco, e garantir que somente usuários identificados consigam usar a API, cada um dentro das permissões do seu perfil.

## Tecnologias

- Python
- FastAPI
- SQLite
- SQLAlchemy ORM
- Pydantic
- Uvicorn
- Swagger / OpenAPI
- passlib + bcrypt (hash de senhas)
- PyJWT (geração e validação dos tokens)
- python-dotenv (leitura das variáveis de ambiente do arquivo `.env`)

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

4. Configure as variáveis de ambiente (veja a seção [Configuração da chave secreta](#configuração-da-chave-secreta)):

   ```bash
   cp .env.example .env
   ```

   No Windows (PowerShell): `Copy-Item .env.example .env`. Depois abra o `.env` e troque os valores.

5. Inicie a API:

   ```bash
   uvicorn main:app --reload
   ```

6. Acesse a documentação interativa:

    - Swagger: http://127.0.0.1:8000/docs
    - OpenAPI: http://127.0.0.1:8000/openapi.json
    - Rota inicial: http://127.0.0.1:8000/

Na primeira inicialização, as tabelas são criadas automaticamente a partir dos modelos SQLAlchemy registrados em `main.py`, e o administrador inicial é criado com os dados do `.env`.

## Configuração da chave secreta

A chave usada para assinar os tokens JWT **não fica no código**. Ela é lida da variável de ambiente `SECRET_KEY`, carregada do arquivo `.env` com o `python-dotenv`. O `.env` está no `.gitignore`, então nenhuma chave real vai para o repositório. O arquivo `.env.example` serve de modelo:

```env
SECRET_KEY=troque_por_uma_chave_secreta_grande
ACCESS_TOKEN_EXPIRE_MINUTES=60

ADMIN_NOME=Administrador
ADMIN_EMAIL=admin@eventos.com
ADMIN_SENHA=troque_esta_senha
```

| Variável | Para que serve |
|---|---|
| `SECRET_KEY` | Chave secreta que assina os tokens. **Obrigatória**: sem ela a API não inicia |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Validade do token em minutos (padrão: 60) |
| `ADMIN_NOME`, `ADMIN_EMAIL`, `ADMIN_SENHA` | Dados do administrador inicial |

Use uma chave longa e aleatória (32 caracteres ou mais). Uma forma simples de gerar:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

## Segurança

### Hash das senhas

A senha nunca é salva como texto. No cadastro, ela passa pelo `CryptContext` do `passlib` com o algoritmo **bcrypt**, e só o hash é salvo na coluna `senha_hash`. No login, a senha digitada é comparada com o hash pela função `verify` da própria biblioteca. Nenhuma resposta da API devolve a senha ou o hash: os schemas de resposta (`UsuarioResponse`) têm apenas `id`, `nome`, `email` e `perfil`.

### Token JWT

Depois do login, a API gera um token JWT assinado com `SECRET_KEY` e o algoritmo **HS256**. O payload tem:

- `sub`: o `id` do usuário;
- `exp`: a data de expiração (agora + `ACCESS_TOKEN_EXPIRE_MINUTES`).

Nas rotas protegidas, o token deve ir no cabeçalho:

```
Authorization: Bearer <token>
```

A validação fica centralizada em `security/security.py`, na dependência `get_current_user`, usada nas rotas com `Depends`. Ela confere se o cabeçalho existe, se a assinatura é válida e se o token não expirou, e então busca o usuário no banco pelo `id` do token. Token ausente, adulterado, assinado com outra chave ou expirado gera `401`.

### Perfis e permissões

Existem dois perfis: `administrador` e `usuario`. A verificação é feita no servidor pela dependência `verificar_admin`, que usa o perfil salvo no banco (e não algo enviado pelo cliente). Quando um usuário autenticado tenta fazer algo que o seu perfil não permite, a API devolve `403`.

**Administrador**
- cadastrar, atualizar e excluir eventos;
- atualizar e excluir participantes;
- consultar eventos, participantes e as inscrições de cada evento;
- consultar os relatórios consolidados;
- tudo o que o usuário comum pode fazer.

**Usuário comum**
- consultar os eventos;
- consultar e cadastrar participantes;
- realizar inscrições em eventos;
- consultar os próprios dados em `/auth/me`.

### Criação do administrador inicial

A rota pública `POST /usuarios` **sempre** cria usuários com o perfil `usuario`. Se alguém mandar `"perfil": "administrador"` no corpo, o campo é ignorado. Assim, ninguém se torna administrador por conta própria.

O primeiro administrador é criado automaticamente quando a aplicação inicia, com os dados de `ADMIN_NOME`, `ADMIN_EMAIL` e `ADMIN_SENHA` do `.env`. Se já existir um usuário com esse e-mail, nada é feito. Se as variáveis não forem preenchidas, nenhum administrador é criado.

## Banco de dados

O projeto utiliza SQLite. A conexão está configurada em `database.py` com o endereço `sqlite:///./eventos.db`. Portanto, o arquivo `eventos.db` é criado na pasta de execução do projeto (normalmente a própria pasta `aps2-api-eventos`).

O arquivo do banco é local e está incluído no `.gitignore` para evitar o envio acidental de dados de execução ao repositório. Ao clonar o projeto em outro computador, a aplicação cria um banco novo na primeira execução. Os dados permanecem salvos entre reinicializações enquanto o arquivo `eventos.db` for mantido.

## Funcionalidades e rotas

Na coluna **Acesso**: *Pública* não exige token; *Autenticado* exige token de qualquer perfil; *Admin* exige token de um administrador.

### Usuários e autenticação

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/usuarios` | Pública | Cadastrar usuário (sempre com perfil `usuario`) |
| POST | `/auth/login` | Pública | Autenticar com e-mail e senha e receber o token JWT |
| GET | `/auth/me` | Autenticado | Consultar os dados do usuário dono do token |

Exemplo de corpo para `POST /usuarios`:

```json
{
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "senha": "senha_segura"
}
```

Resposta (`201`):

```json
{
  "id": 2,
  "nome": "Aluno Exemplo",
  "email": "aluno@exemplo.com",
  "perfil": "usuario"
}
```

Regras do cadastro: nome não pode ser vazio, e-mail precisa ser válido e único, e a senha deve ter entre 6 e 72 caracteres e não pode ser só espaços. O limite de 72 vem do bcrypt, que só considera os primeiros 72 bytes.

Exemplo de corpo para `POST /auth/login`:

```json
{
  "email": "aluno@exemplo.com",
  "senha": "senha_segura"
}
```

Resposta (`200`):

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Se o e-mail não existir ou a senha estiver errada, a resposta é sempre a mesma: `401` com `"E-mail ou senha inválidos."`. Assim, a mensagem não revela qual dos dois está errado.

### Eventos

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/eventos` | Admin | Cadastrar evento |
| GET | `/eventos` | Autenticado | Listar eventos |
| GET | `/eventos/{evento_id}` | Autenticado | Consultar evento pelo ID |
| PUT | `/eventos/{evento_id}` | Admin | Atualizar evento (a capacidade não pode ficar menor que o número de inscritos) |
| DELETE | `/eventos/{evento_id}` | Admin | Excluir evento, se não possuir inscrições |

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

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/participantes` | Autenticado | Cadastrar participante |
| GET | `/participantes` | Autenticado | Listar participantes |
| GET | `/participantes/{participante_id}` | Autenticado | Consultar participante pelo ID |
| PUT | `/participantes/{participante_id}` | Admin | Atualizar participante |
| DELETE | `/participantes/{participante_id}` | Admin | Excluir participante, se não possuir inscrições |

Exemplo de corpo para `POST /participantes`:

```json
{
  "nome": "Joao Silva",
  "email": "joao@email.com",
  "curso": "Engenharia de Software"
}
```

### Inscrições

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| POST | `/eventos/{evento_id}/inscricoes/{participante_id}` | Autenticado | Inscrever participante em evento |
| GET | `/eventos/{evento_id}/inscricoes` | Admin | Listar inscrições de um evento, junto com os dados de cada participante |

A criação da inscrição verifica se o evento e o participante existem, se a inscrição já foi realizada e se ainda há vagas. A combinação de `evento_id` e `participante_id` também possui restrição de unicidade no banco. Se mesmo assim o banco recusar uma inscrição repetida, a API devolve `409` em vez de um erro interno.

### Relatórios

| Método | Rota | Acesso | Informações retornadas |
|---|---|---|---|
| GET | `/relatorios/ocupacao-eventos` | Admin | Capacidade, inscritos, vagas disponíveis e percentual de ocupação por evento |
| GET | `/relatorios/eventos-por-categoria` | Admin | Quantidade de eventos, capacidade total e inscrições por categoria |
| GET | `/relatorios/participacao-por-curso` | Admin | Quantidade de participantes distintos e inscrições por curso |

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
- `200 OK`: consulta, atualização ou login realizado;
- `204 No Content`: exclusão realizada;
- `401 Unauthorized`: credenciais inválidas no login, ou token ausente, inválido ou expirado;
- `403 Forbidden`: usuário autenticado, mas sem permissão para a operação;
- `404 Not Found`: evento ou participante não encontrado;
- `409 Conflict`: e-mail de usuário ou participante já cadastrado, inscrição duplicada, evento sem vagas, capacidade menor que o número de inscritos ou tentativa de excluir registro com inscrições;
- `500 Internal Server Error`: falha inesperada no banco de dados, com uma mensagem simples, sem expor detalhes técnicos;
- `422 Unprocessable Entity`: dados enviados não passaram pela validação.

## Organização do projeto

```text
aps2-api-eventos/
├── main.py
├── database.py
├── requirements.txt
├── README.md
├── .env.example               # modelo das variáveis de ambiente
├── .env                       # criado por você, não vai para o repositório
├── eventos.db                 # criado localmente ao executar a aplicação
├── controllers/
│   ├── auth_controller.py
│   ├── usuario_controller.py
│   ├── evento_controller.py
│   ├── participante_controller.py
│   ├── inscricao_controller.py
│   └── relatorio_controller.py
├── models/
│   ├── usuario.py
│   ├── evento.py
│   ├── participante.py
│   └── inscricao.py
├── schemas/
│   ├── usuario_schema.py
│   ├── evento_schema.py
│   ├── participante_schema.py
│   └── inscricao_schema.py
├── services/
│   ├── auth_service.py
│   ├── usuario_service.py
│   ├── evento_service.py
│   ├── participante_service.py
│   ├── inscricao_service.py
│   └── relatorio_service.py
├── repositories/
│   ├── usuario_repository.py
│   ├── evento_repository.py
│   ├── participante_repository.py
│   ├── inscricao_repository.py
│   └── relatorio_repository.py
└── security/
    └── security.py
```

### Responsabilidade das camadas

- **Controllers:** definem as rotas HTTP, recebem parâmetros e retornam respostas;
- **Schemas:** validam os dados de entrada e definem os formatos de resposta com Pydantic;
- **Models:** representam as tabelas e os relacionamentos no SQLAlchemy;
- **Services:** aplicam as regras de negócio;
- **Repositories:** realizam consultas e operações no banco de dados;
- **Security:** hash e verificação de senhas, geração e validação dos tokens JWT e as dependências `get_current_user` e `verificar_admin`, usadas nas rotas;
- **Database:** configura a conexão, a sessão e a disponibilização do acesso ao SQLite.

A lógica de autenticação e autorização não fica dentro das rotas: cada rota só declara `Depends(get_current_user)` ou `Depends(verificar_admin)`.

## Roteiro de testes pelo Swagger

Com a API em execução, abra http://127.0.0.1:8000/docs.

**Como enviar o token no Swagger:** as rotas protegidas mostram um campo `authorization` (cabeçalho). Depois de fazer login, copie o `access_token` e preencha esse campo com `Bearer ` seguido do token, por exemplo: `Bearer eyJhbGciOi...`.

### Autenticação e segurança

1. **Cadastro de usuário:** `POST /usuarios` com nome, e-mail e senha → `201`. A resposta não tem senha nem hash, e o perfil é `usuario`.
2. **Senha salva como hash:** abra o `eventos.db` (por exemplo, no DB Browser for SQLite) e consulte a tabela `usuarios`. A coluna `senha_hash` guarda algo como `$2b$12$...`, e não a senha digitada.
3. **E-mail duplicado:** repita o mesmo `POST /usuarios` → `409`.
4. **Tentar virar administrador:** envie `"perfil": "administrador"` no corpo de `POST /usuarios` → o usuário é criado com o perfil `usuario`.
5. **Login válido:** `POST /auth/login` com os dados do passo 1 → `200` com `access_token`.
6. **Login inválido:** senha errada ou e-mail inexistente → `401` com a mesma mensagem nos dois casos.
7. **Rota protegida sem token:** `GET /eventos` com o campo `authorization` vazio → `401`.
8. **Rota protegida com token válido:** `GET /eventos` com `Bearer <token>` → `200`.
9. **Token inválido:** altere alguns caracteres do token → `401`.
10. **Token expirado:** coloque `ACCESS_TOKEN_EXPIRE_MINUTES=1` no `.env`, reinicie a API, faça login, espere um pouco mais de 1 minuto e use o token → `401` com `"Token expirado. Faça login novamente."`.
11. **Operação administrativa com usuário comum:** `POST /eventos` com o token do usuário comum → `403`.
12. **Operação administrativa com administrador:** faça login com `ADMIN_EMAIL` / `ADMIN_SENHA` e repita o `POST /eventos` → `201`.
13. **Dados do usuário autenticado:** `GET /auth/me` → `200` com `id`, `nome`, `email` e `perfil`, sem senha.

### Funcionalidades da APS 3 (com as novas regras de acesso)

14. Como administrador: cadastrar, consultar, atualizar e excluir eventos;
15. Como usuário comum: cadastrar um participante e inscrevê-lo em um evento → `201`;
16. Repetir a mesma inscrição → `409`; inscrever em evento ou participante inexistente → `404`;
17. Criar evento com capacidade 1, fazer uma inscrição e tentar uma segunda → `409`;
18. Tentar excluir evento ou participante com inscrições (como admin) → `409`;
19. Como administrador: consultar as inscrições do evento e os três relatórios → `200`. Como usuário comum, as mesmas rotas → `403`;
20. Reiniciar a aplicação e consultar os registros de novo para verificar a persistência.

Os testes mostram, no próprio Swagger, o corpo enviado, o código HTTP devolvido e a resposta JSON.
