# PDF API

API criada como desafio técnico, desenvolvida em FastAPI com SQLite para persistência de dados.

A proposta é simples: enviar um arquivo PDF, extrair o texto dele e poder gerenciar esse conteúdo via API.

---

## Tecnologias

- Python 3.13
- FastAPI
- SQLite + SQLAlchemy
- PyMuPDF (extração de texto)
- JWT (autenticação)

---

## Como rodar

**1. Clone o repositório e entre na pasta**
```bash
git clone https://github.com/Viana0610/pdf-api.git
cd pdf-api
```

**2. Crie o ambiente virtual e ative**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Suba o servidor**
```bash
uvicorn app.main:app --reload
```

Acesse em `http://127.0.0.1:8000/docs`

---

## Como usar

### Autenticação

Todos os endpoints são protegidos. Para acessar:

1. Crie um usuário em `POST /auth/register`
2. Faça login em `POST /auth/token` com seu usuário e senha
3. Clique em **Authorize** no Swagger e preencha usuário e senha

### Endpoints disponíveis

| Método | Rota | O que faz |
|--------|------|-----------|
| POST | `/auth/register` | Cadastra um novo usuário |
| POST | `/auth/token` | Gera o token de acesso |
| POST | `/pdf/upload` | Envia um PDF e extrai o texto |
| GET | `/texts/` | Lista todos os registros |
| GET | `/texts/{id}` | Busca um registro pelo ID |
| PUT | `/texts/{id}` | Atualiza um registro |
| DELETE | `/texts/{id}` | Remove um registro |

---

## Observações

- O banco de dados é criado automaticamente ao rodar a aplicação
- A documentação interativa fica disponível pelo próprio Swagger em `/docs`