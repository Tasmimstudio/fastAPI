from fastapi import APIRouter
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from app.crud import comment as crud_comment

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/post/{post_id}", response_model=CommentResponse)
def create_comment(username: str, post_id: str, comment_data: CommentCreate):
    return crud_comment.create_comment(username, post_id, comment_data)

@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: str):
    return crud_comment.get_comment(comment_id)

@router.get("/post/{post_id}", response_model=list[CommentResponse])
def get_post_comments(post_id: str):
    return crud_comment.get_post_comments(post_id)

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(comment_id: str, username: str, comment_data: CommentUpdate):
    return crud_comment.update_comment(comment_id, username, comment_data)

@router.delete("/{comment_id}")
def delete_comment(comment_id: str, username: str):
    return crud_comment.delete_comment(comment_id, username)