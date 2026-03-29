from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token
from app.auth import authenticate_user, create_access_token, get_password_hash, get_user, ACCESS_TOKEN_EXPIRE_MINUTES
from app.routers import pdf, texts

# Cria as tabelas no banco automaticamente ao iniciar a aplicação
Base.metadata.create_all(bind=engine)

description = """
## Sobre

API para upload e gerenciamento de textos extraídos de arquivos PDF.

## Como usar

1. Crie um usuário em `/auth/register`
2. Faça login em `/auth/token` e copie o token
3. Clique em **Authorize** e cole o token
4. Utilize os endpoints de PDF e Texts

## Endpoints disponíveis

- **Auth** — Cadastro e login de usuários
- **PDF** — Upload e extração de texto de arquivos PDF
- **Texts** — Gerenciamento dos textos extraídos (CRUD completo)
"""

# Inicializa a aplicação com as informações que aparecem no Swagger
app = FastAPI(
    title="PDF API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Lucas Viana",
        "url": "https://github.com/Viana0610/pdf-api",
    }
)

# Endpoint para cadastrar um novo usuário
@app.post(
    "/auth/register",
    response_model=UserResponse,
    tags=["Auth"],
    summary="Cadastrar usuário",
    description="Cria um novo usuário com username e senha. A senha é armazenada com hash bcrypt."
)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Verifica se o username já está cadastrado
    existing = get_user(db, user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username ja cadastrado")

    # Salva o usuário com a senha criptografada
    user = User(
        username=user_data.username,
        hashed_password=get_password_hash(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Endpoint de login que retorna o token JWT
@app.post(
    "/auth/token",
    response_model=Token,
    tags=["Auth"],
    summary="Login",
    description="Autentica o usuário e retorna um token JWT válido por 30 minutos."
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Valida as credenciais no banco
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Gera e retorna o token com tempo de expiração
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Registra os routers de PDF e CRUD de textos
app.include_router(pdf.router)
app.include_router(texts.router)

# Rota raiz para verificar se a API está no ar
@app.get("/", tags=["Root"], summary="Status da API", description="Verifica se a API está funcionando.")
def root():
    return {"message": "PDF API funcionando!"}