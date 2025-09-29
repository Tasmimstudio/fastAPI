from app.models.like import Like
from app.models.post import Post
from app.models.comment import Comment
from app.models.user import User
from app.schemas.like import LikeResponse
from fastapi import HTTPException

def like_post(username: str, post_id: str):
    try:
        user = User.nodes.get(username=username)
        post = Post.nodes.get(element_id_property=post_id)

        existing_like = Like.nodes.filter(like_type="post").filter(
            user__username=username
        ).filter(post__element_id_property=post_id).first()

        if existing_like:
            raise HTTPException(status_code=400, detail="Post already liked")

        like = Like(like_type="post").save()
        like.user.connect(user)
        like.post.connect(post)

        post.likes_count += 1
        post.save()

        return {"message": "Post liked successfully"}
    except (User.DoesNotExist, Post.DoesNotExist):
        raise HTTPException(status_code=404, detail="User or Post not found")

def unlike_post(username: str, post_id: str):
    try:
        user = User.nodes.get(username=username)
        post = Post.nodes.get(element_id_property=post_id)

        like = Like.nodes.filter(like_type="post").filter(
            user__username=username
        ).filter(post__element_id_property=post_id).first()

        if not like:
            raise HTTPException(status_code=400, detail="Post not liked yet")

        like.delete()
        post.likes_count = max(0, post.likes_count - 1)
        post.save()

        return {"message": "Post unliked successfully"}
    except (User.DoesNotExist, Post.DoesNotExist):
        raise HTTPException(status_code=404, detail="User or Post not found")

def like_comment(username: str, comment_id: str):
    try:
        user = User.nodes.get(username=username)
        comment = Comment.nodes.get(element_id_property=comment_id)

        existing_like = Like.nodes.filter(like_type="comment").filter(
            user__username=username
        ).filter(comment__element_id_property=comment_id).first()

        if existing_like:
            raise HTTPException(status_code=400, detail="Comment already liked")

        like = Like(like_type="comment").save()
        like.user.connect(user)
        like.comment.connect(comment)

        comment.likes_count += 1
        comment.save()

        return {"message": "Comment liked successfully"}
    except (User.DoesNotExist, Comment.DoesNotExist):
        raise HTTPException(status_code=404, detail="User or Comment not found")

def unlike_comment(username: str, comment_id: str):
    try:
        user = User.nodes.get(username=username)
        comment = Comment.nodes.get(element_id_property=comment_id)

        like = Like.nodes.filter(like_type="comment").filter(
            user__username=username
        ).filter(comment__element_id_property=comment_id).first()

        if not like:
            raise HTTPException(status_code=400, detail="Comment not liked yet")

        like.delete()
        comment.likes_count = max(0, comment.likes_count - 1)
        comment.save()

        return {"message": "Comment unliked successfully"}
    except (User.DoesNotExist, Comment.DoesNotExist):
        raise HTTPException(status_code=404, detail="User or Comment not found")