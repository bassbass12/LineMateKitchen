from fastapi import APIRouter, HTTPException
from app.models.document import Document

router = APIRouter(prefix="/documents", tags=["Documents"])
from app.data_loader import load_documents

documents = load_documents()

@router.get("/", response_model=list[Document])
def get_documents():
    return documents

@router.post("/", response_model=Document)
def create_document(document: Document):
    documents.append(document)
    return document

@router.get("/{document_id}", response_model=Document)
def get_document(document_id: int):
    for document in documents:
        if document.id == document_id:
            return document

    raise HTTPException(status_code=404, detail="Document not found")


@router.delete("/{document_id}")
def delete_document(document_id: int):
    for document in documents:
        if document.id == document_id:
            documents.remove(document)
            return {"message": "Document deleted"}

    raise HTTPException(status_code=404, detail="Document not found")