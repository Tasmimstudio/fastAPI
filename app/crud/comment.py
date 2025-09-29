from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from fastapi import HTTPException

def create_comment(username: str, post_id: str, data: CommentCreate):
    try:
        user = User.nodes.get(username=username)
        post = Post.nodes.get(element_id_property=post_id)

        comment = Comment(content=data.content).save()
        comment.author.connect(user)
        comment.post.connect(post)

        if data.parent_comment_id:
            parent_comment = Comment.nodes.get(element_id_property=data.parent_comment_id)
            comment.parent_comment.connect(parent_comment)

        post.comments_count = len(post.comments)
        post.save()

        return CommentResponse(
            element_id_property=comment.element_id_property,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            likes_count=comment.likes_count,
            author_username=username,
            parent_comment_id=data.parent_comment_id
        )
    except (User.DoesNotExist, Post.DoesNotExist):
        raise HTTPException(status_code=404, detail="User or Post not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Comment creation failed: {str(e)}")

def get_comment(comment_id: str):
    try:
        comment = Comment.nodes.get(element_id_property=comment_id)
        author = comment.author.single() if comment.author else None
        parent = comment.parent_comment.single() if comment.parent_comment else None

        return CommentResponse(
            element_id_property=comment.element_id_property,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            likes_count=comment.likes_count,
            author_username=author.username if author else None,
            parent_comment_id=parent.element_id_property if parent else None,
            replies_count=len(comment.replies)
        )
    except Comment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

def get_post_comments(post_id: str):
    try:
        post = Post.nodes.get(element_id_property=post_id)
        comments = post.comments.all()

        result = []
        for comment in comments:
            author = comment.author.single() if comment.author else None
            parent = comment.parent_comment.single() if comment.parent_comment else None

            result.append(CommentResponse(
                element_id_property=comment.element_id_property,
                content=comment.content,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
                likes_count=comment.likes_count,
                author_username=author.username if author else None,
                parent_comment_id=parent.element_id_property if parent else None,
                replies_count=len(comment.replies)
            ))
        return result
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

def update_comment(comment_id: str, username: str, data: CommentUpdate):
    try:
        comment = Comment.nodes.get(element_id_property=comment_id)
        author = comment.author.single()

        if not author or author.username != username:
            raise HTTPException(status_code=403, detail="Not authorized to update this comment")

        comment.content = data.content
        comment.save()

        return CommentResponse(
            element_id_property=comment.element_id_property,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            likes_count=comment.likes_count,
            author_username=username
        )
    except Comment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")

def delete_comment(comment_id: str, username: str):
    try:
        comment = Comment.nodes.get(element_id_property=comment_id)
        author = comment.author.single()

        if not author or author.username != username:
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")

        post = comment.post.single()
        if post:
            post.comments_count = max(0, post.comments_count - 1)
            post.save()

        comment.delete()
        return {"message": "Comment deleted successfully"}
    except Comment.DoesNotExist:
        raise HTTPException(status_code=404, detail="Comment not found")