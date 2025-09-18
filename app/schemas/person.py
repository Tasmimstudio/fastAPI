from pydantic import BaseModel
from typing import List, Optional

class PersonCreate(BaseModel):
    name: str
    age: int

class PersonResponse(BaseModel):
    element_id_property: str 
    name: str
    age: int

    friends: Optional[List[str]] = []  # list of friend names

    @classmethod
    def from_orm(cls, person):
        return cls(
            id=person.element_id_property,
            name=person.name,
            age=person.age,
            friends=[f.name for f in person.friends]  # resolve friend names
        )
