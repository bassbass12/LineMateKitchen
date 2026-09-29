from pydantic import BaseModel
from datetime import datetime

class Ticket(BaseModel):
    id: int
    title: str
    priority: str
    status: str
    assignee_id: int | None = None
    related_document_id: int | None = None
    created_at: datetime
