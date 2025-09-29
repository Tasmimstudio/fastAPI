from fastapi import APIRouter
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.crud import post as crud_post

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse)
def create_post(username: str, post_data: PostCreate):
    return crud_post.create_post(username, post_data)

@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: str):
    return crud_post.get_post(post_id)

@router.get("/", response_model=list[PostResponse])
def list_posts():
    return crud_post.list_posts()

@router.get("/user/{username}", response_model=list[PostResponse])
def get_user_posts(username: str):
    return crud_post.get_user_posts(username)

@router.put("/{post_id}")
def update_post(post_id: str, username: str, post_data: PostUpdate):
    return crud_post.update_post(post_id, username, post_data)

@router.delete("/{post_id}")
def delete_post(post_id: str, username: str):
    return crud_post.delete_post(post_id, username)