from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema para criação de usuário (dados que chegam na requisição)
class UserCreate(BaseModel):
    username: str
    password: str

# Schema para resposta de usuário (nunca retorna a senha)
class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  # Permite converter objeto do banco em JSON

# Schema base com os campos compartilhados do texto extraído
class ExtractedTextBase(BaseModel):
    filename: str
    content: str

# Schema para criação de texto (herda o base sem alterações)
class ExtractedTextCreate(ExtractedTextBase):
    pass

# Schema para atualização parcial (todos os campos são opcionais)
class ExtractedTextUpdate(BaseModel):
    filename: Optional[str] = None
    content: Optional[str] = None

# Schema para resposta completa (inclui id e datas)
class ExtractedTextResponse(ExtractedTextBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite converter objeto do banco em JSON

# Schema do token retornado após o login
class Token(BaseModel):
    access_token: str
    token_type: str

# Schema dos dados dentro do token JWT
class TokenData(BaseModel):
    username: Optional[str] = None