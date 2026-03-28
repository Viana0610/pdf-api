from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ExtractedText
from app.schemas import ExtractedTextResponse, ExtractedTextUpdate
from app.auth import get_current_user

router = APIRouter(prefix="/texts", tags=["Texts"])

@router.get(
    "/",
    response_model=List[ExtractedTextResponse],
    summary="Listar textos",
    description="Retorna todos os textos extraídos salvos no banco de dados."
)
def list_texts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return db.query(ExtractedText).limit(100).all()

@router.get(
    "/{text_id}",
    response_model=ExtractedTextResponse,
    summary="Buscar texto",
    description="Busca um texto específico pelo ID."
)
def get_text(
    text_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    text = db.query(ExtractedText).filter(ExtractedText.id == text_id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Registro nao encontrado")
    return text

@router.put(
    "/{text_id}",
    response_model=ExtractedTextResponse,
    summary="Atualizar texto",
    description="Atualiza parcialmente um registro existente. Apenas os campos enviados serão alterados."
)
def update_text(
    text_id: int,
    text_update: ExtractedTextUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    text = db.query(ExtractedText).filter(ExtractedText.id == text_id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Registro nao encontrado")

    # Atualiza apenas os campos que foram enviados na requisição
    if text_update.filename is not None:
        text.filename = text_update.filename
    if text_update.content is not None:
        text.content = text_update.content

    db.commit()
    db.refresh(text)
    return text

@router.delete(
    "/{text_id}",
    summary="Deletar texto",
    description="Remove permanentemente um registro do banco de dados pelo ID."
)
def delete_text(
    text_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    text = db.query(ExtractedText).filter(ExtractedText.id == text_id).first()
    if not text:
        raise HTTPException(status_code=404, detail="Registro nao encontrado")

    db.delete(text)
    db.commit()
    return {"message": "Registro deletado com sucesso"}