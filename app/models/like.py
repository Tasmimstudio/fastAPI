from neomodel import (
    StructuredNode, StringProperty,
    DateTimeProperty, RelationshipTo
)
from datetime import datetime

class Like(StructuredNode):
    created_at = DateTimeProperty(default_now=True)
    like_type = StringProperty(required=True)

    user = RelationshipTo("User", "LIKED_BY")
    post = RelationshipTo("Post", "LIKED_POST")
    comment = RelationshipTo("Comment", "LIKED_COMMENT")