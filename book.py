from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid
from bson import ObjectId
from database import db
from typing import List, Optional

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
    uploader_id: str
    is_public: bool = True
    
    class Config:
        allow_population_by_field_name = True

class BookManager:
    def add_book(self,book:Book):
        """添加新书"""
        result=db.books.insert_one(book.dict())
        return str(result.inserted_id)
    def get_book(self,book_id):
        """获取单本书籍信息"""
        book_data=db.books.find_one({"_id":ObjectId(book_id)})
        return Book(**book_data) if book_data else None
    def get_books(self, category: Optional[str] = None) -> List[Book]:
        """获取书籍列表"""
        query = {'category': category} if category else {}
        return [Book(**book) for book in self.books.find(query)]

    def search_books(self, query: str) -> List[Book]:
        """搜索书籍"""
        regex_query = {'$regex': query, '$options': 'i'}
        books = self.books.find({
            '$or': [
                {'title': regex_query},
                {'author': regex_query}
            ]
        })
        return [Book(**book) for book in books]
    
    def update_book(self, book_id: str, updates: dict) -> bool:
        """更新书籍信息"""
        result = self.books.update_one(
            {'_id': ObjectId(book_id)},
            {'$set': updates}
        )
        return result.modified_count > 0
    
    def delete_book(self, book_id: str) -> bool:
        """删除书籍"""
        result = db.books.delete_one({'_id': ObjectId(book_id)})
        return result.deleted_count > 0

