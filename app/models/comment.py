from datetime import datetime
from pydantic import BaseModel


class Comment(BaseModel):
    id: int
    ticket_id: int
    author_id: int
    body: str
    created_at: datetime