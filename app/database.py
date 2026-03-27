from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Caminho do banco de dados SQLite (cria o arquivo automaticamente)
SQLALCHEMY_DATABASE_URL = "sqlite:///./pdf_api.db"

# Cria a conexão com o banco
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Responsável por abrir e fechar sessões com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base que os models vão herdar para virar tabelas
Base = declarative_base()

# Função que fornece a sessão do banco para os endpoints
# O "yield" garante que a sessão é fechada após cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()