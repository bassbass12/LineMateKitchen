from fastapi import APIRouter
from app.models.document import Document

router = APIRouter(prefix="/documents", tags=["Documents"])

documents = []

@router.get("/", response_model=list[Document])
def get_documents():
    return documents

@router.post("/", response_model=Document)
def create_document(document: Document):
    documents.append(document)
    return document
