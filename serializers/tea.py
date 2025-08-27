from pydantic import BaseModel
from typing import Optional, List
from .comment import CommentSchema
from .user import UserSchema

class TeaSchema(BaseModel):
  id: Optional[int] = True
  name: str
  in_stock: bool
  rating: int
  user: UserSchema
  comments: List[CommentSchema] = []

  class Config:
    orm_mode = True

class TeaCreate(BaseModel):
    name: str
    in_stock: bool
    rating: int