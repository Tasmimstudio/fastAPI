from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from fastapi import HTTPException
from neomodel import db

def create_post(username: str, data: PostCreate):
    try:
        user = User.nodes.get(username=username)
        post = Post(
            content=data.content,
            image_url=data.image_url
        ).save()
        post.author.connect(user)

        return PostResponse(
            element_id_property=post.element_id_property,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes_count=post.likes_count,
            comments_count=post.comments_count,
            author_username=username
        )
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Post creation failed: {str(e)}")

def get_post(post_id: str):
    try:
        post = Post.nodes.get(element_id_property=post_id)
        author = post.author.single() if post.author else None

        return PostResponse(
            element_id_property=post.element_id_property,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes_count=post.likes_count,
            comments_count=post.comments_count,
            author_username=author.username if author else None
        )
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

def list_posts():
    posts = Post.nodes.all()
    result = []
    for post in posts:
        author = post.author.single() if post.author else None
        result.append(PostResponse(
            element_id_property=post.element_id_property,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes_count=post.likes_count,
            comments_count=post.comments_count,
            author_username=author.username if author else None
        ))
    return result

def get_user_posts(username: str):
    try:
        user = User.nodes.get(username=username)
        posts = user.posts.all()
        return [PostResponse(
            element_id_property=post.element_id_property,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes_count=post.likes_count,
            comments_count=post.comments_count,
            author_username=username
        ) for post in posts]
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

def update_post(post_id: str, username: str, data: PostUpdate):
    try:
        post = Post.nodes.get(element_id_property=post_id)
        author = post.author.single()

        if not author or author.username != username:
            raise HTTPException(status_code=403, detail="Not authorized to update this post")

        if data.content is not None:
            post.content = data.content
        if data.image_url is not None:
            post.image_url = data.image_url
        post.save()

        return PostResponse(
            element_id_property=post.element_id_property,
            content=post.content,
            image_url=post.image_url,
            created_at=post.created_at,
            updated_at=post.updated_at,
            likes_count=post.likes_count,
            comments_count=post.comments_count,
            author_username=username
        )
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

def delete_post(post_id: str, username: str):
    try:
        post = Post.nodes.get(element_id_property=post_id)
        author = post.author.single()

        if not author or author.username != username:
            raise HTTPException(status_code=403, detail="Not authorized to delete this post")

        post.delete()
        return {"message": "Post deleted successfully"}
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")