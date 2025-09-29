from fastapi import APIRouter
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.crud import user as crud_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate):
    return crud_user.create_user(user_data)

@router.get("/{username}", response_model=UserResponse)
def get_user(username: str):
    return crud_user.get_user(username)

@router.get("/", response_model=list[UserResponse])
def list_users():
    return crud_user.list_users()

@router.put("/{username}", response_model=UserResponse)
def update_user(username: str, user_data: UserUpdate):
    return crud_user.update_user(username, user_data)

@router.delete("/{username}")
def delete_user(username: str):
    return crud_user.delete_user(username)

@router.post("/{username}/follow/{target_username}")
def follow_user(username: str, target_username: str):
    return crud_user.follow_user(username, target_username)

@router.delete("/{username}/follow/{target_username}")
def unfollow_user(username: str, target_username: str):
    return crud_user.unfollow_user(username, target_username)