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
git clone 
cd pdf_api
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
Todos os endpoints são protegidos. Para acessar, primeiro gere um token em `POST /auth/token` com:
- **username:** admin
- **password:** admin123

No Swagger, clique em **Authorize** e cole o token.

### Endpoints disponíveis

| Método | Rota | O que faz |
|--------|------|-----------|
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
- Por se tratar de um projeto de estudo, o usuário de autenticação é fixo