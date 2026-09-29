from pydantic import BaseModel
from datetime import datetime

class Document(BaseModel):
    id: int
    title: str
    category: str
    body: str
    owner_id: int | None = None
    last_reviewed_at: datetime | None = None
