from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from fastapi import HTTPException

def create_user(data: UserCreate):
    try:
        user = User(
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            bio=data.bio,
            avatar_url=data.avatar_url,
            location=data.location,
            website=data.website
        ).save()
        return UserResponse(
            element_id_property=user.element_id_property,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            location=user.location,
            website=user.website,
            created_at=user.created_at,
            is_active=user.is_active
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User creation failed: {str(e)}")

def get_user(username: str):
    try:
        user = User.nodes.get(username=username)
        return UserResponse(
            element_id_property=user.element_id_property,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            location=user.location,
            website=user.website,
            created_at=user.created_at,
            is_active=user.is_active,
            followers_count=len(user.followers),
            following_count=len(user.following),
            posts_count=len(user.posts)
        )
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def list_users():
    users = User.nodes.all()
    return [UserResponse(
        element_id_property=user.element_id_property,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        bio=user.bio,
        avatar_url=user.avatar_url,
        location=user.location,
        website=user.website,
        created_at=user.created_at,
        is_active=user.is_active
    ) for user in users]

def update_user(username: str, data: UserUpdate):
    try:
        user = User.nodes.get(username=username)
        if data.full_name is not None:
            user.full_name = data.full_name
        if data.bio is not None:
            user.bio = data.bio
        if data.avatar_url is not None:
            user.avatar_url = data.avatar_url
        if data.location is not None:
            user.location = data.location
        if data.website is not None:
            user.website = data.website
        user.save()
        return UserResponse(
            element_id_property=user.element_id_property,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            bio=user.bio,
            avatar_url=user.avatar_url,
            location=user.location,
            website=user.website,
            created_at=user.created_at,
            is_active=user.is_active
        )
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def delete_user(username: str):
    try:
        user = User.nodes.get(username=username)
        user.delete()
        return {"message": f"User {username} deleted successfully"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def follow_user(username: str, target_username: str):
    try:
        user = User.nodes.get(username=username)
        target_user = User.nodes.get(username=target_username)

        if user.following.is_connected(target_user):
            raise HTTPException(status_code=400, detail="Already following this user")

        user.following.connect(target_user)
        return {"message": f"{username} is now following {target_username}"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def unfollow_user(username: str, target_username: str):
    try:
        user = User.nodes.get(username=username)
        target_user = User.nodes.get(username=target_username)

        if not user.following.is_connected(target_user):
            raise HTTPException(status_code=400, detail="Not following this user")

        user.following.disconnect(target_user)
        return {"message": f"{username} unfollowed {target_username}"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")