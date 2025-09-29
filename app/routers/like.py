from fastapi import APIRouter
from app.crud import like as crud_like

router = APIRouter(prefix="/likes", tags=["Likes"])

@router.post("/post/{post_id}")
def like_post(username: str, post_id: str):
    return crud_like.like_post(username, post_id)

@router.delete("/post/{post_id}")
def unlike_post(username: str, post_id: str):
    return crud_like.unlike_post(username, post_id)

@router.post("/comment/{comment_id}")
def like_comment(username: str, comment_id: str):
    return crud_like.like_comment(username, comment_id)

@router.delete("/comment/{comment_id}")
def unlike_comment(username: str, comment_id: str):
    return crud_like.unlike_comment(username, comment_id)