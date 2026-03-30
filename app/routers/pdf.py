import fitz  # PyMuPDF - biblioteca para leitura de arquivos PDF
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ExtractedText
from app.schemas import ExtractedTextResponse
from app.auth import get_current_user

# Router responsavel pelos endpoints de PDF
# prefix="/pdf" adiciona /pdf automaticamente em todas as rotas
# tags=["PDF"] agrupa os endpoints na categoria PDF no Swagger
router = APIRouter(prefix="/pdf", tags=["PDF"])

# Endpoint que recebe o PDF, extrai o texto e salva no banco
@router.post(
    "/upload",
    response_model=ExtractedTextResponse,
    summary="Upload de PDF",
    description="Recebe um arquivo PDF, extrai o texto de todas as páginas e salva no banco de dados."
)
async def upload_pdf(
    file: UploadFile = File(...), # Arquivo enviado pelo usuário
    db: Session = Depends(get_db), # Sessão do banco de dados
    current_user=Depends(get_current_user) # Exige autenticação
):
    # Valida se o arquivo enviado é realmente um PDF pelo MIME type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")

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

    # Rejeita PDFs que não contém texto
    if not text.strip():
        raise HTTPException(status_code=400, detail="Nenhum texto encontrado no PDF")

    # Salva o texto extraído no banco de dados
    db_text = ExtractedText(filename=file.filename, content=text)
    db.add(db_text)
    db.commit()
    db.refresh(db_text)

    return db_text