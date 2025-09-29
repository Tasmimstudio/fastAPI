from neomodel import (
    StructuredNode, StringProperty, IntegerProperty,
    DateTimeProperty, RelationshipTo, RelationshipFrom
)
from datetime import datetime

class Post(StructuredNode):
    content = StringProperty(required=True)
    image_url = StringProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    likes_count = IntegerProperty(default=0)
    comments_count = IntegerProperty(default=0)

    author = RelationshipTo("User", "POSTED_BY")
    comments = RelationshipFrom("Comment", "ON_POST")
    likes = RelationshipFrom("Like", "LIKED_POST")