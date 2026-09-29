from fastapi import APIRouter, HTTPException
from app.models.comment import Comment
from app.data_loader import load_comments, save_comments

router = APIRouter(prefix="/comments", tags=["Comments"])

comments = load_comments()


@router.get("/", response_model=list[Comment])
def get_comments():
    return comments

@router.post("/", response_model=Comment)
def create_comment(comment: Comment):
    for existing_comment in comments:
        if existing_comment.id == comment.id:
            raise HTTPException(
                status_code=409,
                detail="Comment ID already exists"
            )

    comments.append(comment)
    save_comments(comments)

    return comment