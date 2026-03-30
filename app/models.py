from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone, timedelta
from app.database import Base

# Fuso horário de Brasília (UTC-3)
def brasilia_now():
    return datetime.now(timezone(timedelta(hours=-3))).replace(tzinfo=None)

# Tabela de usuários para autenticação
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)  # Senha salva com hash, nunca em texto puro

# Tabela que armazena os textos extraídos dos PDFs
class ExtractedText(Base):
    __tablename__ = "extracted_texts"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)        # Nome do arquivo PDF enviado
    content = Column(Text, nullable=False)            # Texto extraído do PDF
    created_at = Column(DateTime, default=brasilia_now)                          # Data de criação
    updated_at = Column(DateTime, default=brasilia_now, onupdate=brasilia_now)   # Última atualização