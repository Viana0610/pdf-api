import fitz  # PyMuPDF - biblioteca para leitura de arquivos PDF
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ExtractedText
from app.schemas import ExtractedTextResponse
from app.auth import get_current_user

router = APIRouter(prefix="/pdf", tags=["PDF"])

@router.post("/upload", response_model=ExtractedTextResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)  # Exige autenticação
):
    # Valida se o arquivo enviado é realmente um PDF pelo MIME type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF sao aceitos")

    # Lê o conteúdo do arquivo enviado
    contents = await file.read()

    try:
        # Abre o PDF em memória e extrai o texto página por página
        doc = fitz.open(stream=contents, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar PDF: {str(e)}")

    # Rejeita PDFs que não contém texto (ex: PDFs escaneados sem OCR)
    if not text.strip():
        raise HTTPException(status_code=400, detail="Nenhum texto encontrado no PDF")

    # Salva o texto extraído no banco de dados
    db_text = ExtractedText(filename=file.filename, content=text)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)

    return db_text