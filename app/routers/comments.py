from fastapi import APIRouter
from app.models.comment import Comment

router = APIRouter(prefix="/comments", tags=["Comments"])

from app.data_loader import load_comments

comments = load_comments()

@router.get("/", response_model=list[Comment])
def get_comments():
    return comments


@router.post("/", response_model=Comment)
def create_comment(comment: Comment):
    comments.append(comment)
    return comment