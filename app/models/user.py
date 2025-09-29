from neomodel import (
    StructuredNode, StringProperty, IntegerProperty,
    DateTimeProperty, RelationshipTo, RelationshipFrom
)
from datetime import datetime

class User(StructuredNode):
    username = StringProperty(unique_index=True, required=True)
    email = StringProperty(unique_index=True, required=True)
    full_name = StringProperty()
    bio = StringProperty()
    avatar_url = StringProperty()
    location = StringProperty()
    website = StringProperty()
    created_at = DateTimeProperty(default_now=True)
    updated_at = DateTimeProperty(default_now=True)
    is_active = StringProperty(default="true")

    following = RelationshipTo("User", "FOLLOWS")
    followers = RelationshipFrom("User", "FOLLOWS")
    posts = RelationshipFrom("Post", "POSTED_BY")