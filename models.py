from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from typing import List, Optional
from bson import ObjectId

class Book(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    title: str
    author: str
    category: str
    cover_path: Optional[str] = None
    file_path: str
    file_size: int
    file_type: str
    upload_time: datetime = Field(default_factory=datetime.utcnow)
    #uploader_id: str
    is_public: bool = True
    class Config:
        allow_population_by_field_name = True

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    user_id:str
    username: str
    email: str
    password: str
    role: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    is_active: bool = True
    class Config:
        allow_population_by_field_name = True