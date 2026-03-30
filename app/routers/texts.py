from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ExtractedText
from app.schemas import ExtractedTextResponse, ExtractedTextUpdate
from app.auth import get_current_user

# Router responsavel pelos endpoints de CRUD dos textos extraidos
# prefix="/texts" adiciona /texts automaticamente em todas as rotas
# tags=["Texts"] agrupa os endpoints na categoria Texts no Swagger
router = APIRouter(prefix="/texts", tags=["Texts"])


# Endpoint: GET /texts/
# Lista todos os textos extraidos que estao salvos no banco de dados
# Retorna uma lista de registros com id, filename, content e datas
# Limitado a 100 registros por requisicao para nao sobrecarregar a API
# Requer autenticacao via token JWT
@router.get(
    "/",
    response_model=List[ExtractedTextResponse],
    summary="Listar textos",
    description="Retorna todos os textos extraidos salvos no banco de dados."
)
def list_texts(
    db: Session = Depends(get_db),          # Sessao do banco de dados
    current_user=Depends(get_current_user)  # Exige autenticacao via token JWT
):
    # Busca todos os registros da tabela limitando a 100 resultados
    return db.query(ExtractedText).limit(100).all()


# Endpoint: GET /texts/{text_id}
# Busca um unico registro pelo ID informado na URL
# Se o ID existir, retorna o registro completo com todos os campos
# Se o ID nao existir, retorna erro 404 — registro nao encontrado
# Requer autenticacao via token JWT
@router.get(
    "/{text_id}",
    response_model=ExtractedTextResponse,
    summary="Buscar texto",
    description="Busca um texto especifico pelo ID."
)
def get_text(
    text_id: int,                            # ID informado na URL
    db: Session = Depends(get_db),           # Sessao do banco de dados
    current_user=Depends(get_current_user)   # Exige autenticacao via token JWT
):
    # Filtra o registro pelo ID e retorna o primeiro resultado encontrado
    text = db.query(ExtractedText).filter(ExtractedText.id == text_id).first()
    if not text:
        # Registro nao encontrado — retorna erro 404
        raise HTTPException(status_code=404, detail="Registro nao encontrado")
    return text


# Endpoint: PUT /texts/{text_id}
# Atualiza parcialmente um registro existente pelo ID
# Aceita filename, content ou ambos — so atualiza o que for enviado
# Os campos nao enviados permanecem com o valor original no banco
# Se o ID nao existir, retorna erro 404 — registro nao encontrado
# Requer autenticacao via token JWT
@router.put(
    "/{text_id}",
    response_model=ExtractedTextResponse,
    summary="Atualizar texto",
    description="Atualiza parcialmente um registro existente. Apenas os campos enviados serao alterados."
)
def update_text(
    text_id: int,                            # ID informado na URL
    text_update: ExtractedTextUpdate,        # Campos a serem atualizados
    db: Session = Depends(get_db),           # Sessao do banco de dados
    current_user=Depends(get_current_user)   # Exige autenticacao via token JWT
):
    # Busca o registro pelo ID
    text = db.query(ExtractedText).filter(ExtractedText.id == text_id).first()
    if not text:
        # Registro nao encontrado — retorna erro 404
        raise HTTPException(status_code=404, detail="Registro nao encontrado")

    # Verifica cada campo — so atualiza se foi enviado na requisicao
    # Se o campo for None significa que nao foi enviado, entao mantem o valor original
    if text_update.filename is not None:
        text.filename = text_update.filename
    if text_update.content is not None:
        text.content = text_update.content

    # Salva as alteracoes no banco
    db.commit()
    # Atualiza o objeto Python com os dados mais recentes do banco
    db.refresh(text)
    return text


# Endpoint: DELETE /texts/{text_id}
# Remove permanentemente um registro do banco pelo ID
# A operacao nao tem volta — o registro e deletado definitivamente
# Nao remove o arquivo PDF original, apenas o registro do texto extraido
# Se o ID nao existir, retorna erro 404 — registro nao encontrado
# Requer autenticacao via token JWT
@router.delete(
    "/{text_id}",
    summary="Deletar texto",
    description="Remove permanentemente um registro do banco de dados pelo ID."
)
def delete_text(
    text_id: int,                            # ID informado na URL
    db: Session = Depends(get_db),           # Sessao do banco de dados
    current_user=Depends(get_current_user)   # Exige autenticacao via token JWT
):
    # Busca o registro pelo ID
    text = db.query(ExtractedText).filter(ExtractedText.id == text_id).first()
    if not text:
        # Registro nao encontrado — retorna erro 404
        raise HTTPException(status_code=404, detail="Registro nao encontrado")

    # Remove o registro do banco
    db.delete(text)
    # Confirma a operacao — sem o commit o delete nao e salvo
    db.commit()
    return {"message": "Registro deletado com sucesso"}