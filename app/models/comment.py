from neomodel import (
    StructuredNode, StringProperty, IntegerProperty,
    DateTimeProperty, RelationshipTo, RelationshipFrom
)
from datetime import datetime

class Comment(StructuredNode):
    content = StringProperty(required=True)
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    likes_count = IntegerProperty(default=0)

    author = RelationshipTo("User", "COMMENTED_BY")
    post = RelationshipTo("Post", "ON_POST")
    likes = RelationshipFrom("Like", "LIKED_COMMENT")
    parent_comment = RelationshipTo("Comment", "REPLY_TO")
    replies = RelationshipFrom("Comment", "REPLY_TO")