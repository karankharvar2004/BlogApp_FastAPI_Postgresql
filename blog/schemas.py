from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class BlogBase(BaseModel):
    title: str
    content: str
    author: str

class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None


class BlogResponse(BlogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True