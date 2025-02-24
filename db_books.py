from pymongo import MongoClient
from models import Book
from typing import List, Optional
from bson import ObjectId
from PIL import Image
import os
import io
from config.setting import MONGODB_URL, MONGODB_DB_NAME

def save_book_file(file) -> str:
    """保存书籍文件"""
    file_path = f"uploads/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    return file_path

def save_cover(file) -> str:
        """保存并处理封面图片"""
        cover_path = f"book_covers/{file.name}"
        image = Image.open(file)
        image = image.convert('RGB')
        image = image.resize((200, 300), Image.Resampling.LANCZOS)
        image.save(cover_path, 'PNG')
        return cover_path

def get_default_cover():
    # 返回默认封面图片
    default_cover = Image.new('RGB', (200, 300), 'gray')
    img_byte_arr = io.BytesIO()
    default_cover.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

class BookManager:
    def __init__(
            self, 
            db_url=MONGODB_URL,
            db_name=MONGODB_DB_NAME
    ):
        # MongoDB 连接
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.books = self.db.books

    def add_book(
            self, 
            title:str,
            author:str,
            category:str,
            book_file,
            cover_file
            #uploader_id:str,
           
            ):
        """添加新书"""
        try:
            # 保存文件
            file_path = save_book_file(book_file)
            cover_path = save_cover(cover_file) if cover_file else None
            book = Book(
                title=title,
                author=author,
                category=category,
                file_path=file_path,
                cover_path=cover_path,
                file_size=os.path.getsize(file_path),
                file_type=book_file.type
                #uploader_id=uploader_id
            )
        
            self.books.insert_one(book.dict())
            return True, "书籍添加成功"
        except Exception as e:
            return False, f"书籍添加失败: {str(e)}"

    def get_book(self, book_id: str) -> Optional[Book]:
        """获取单本书籍信息"""
        book_data = self.books.find_one({"_id": ObjectId(book_id)})
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
        #result = self.books.delete_one({'_id': ObjectId(book_id)})
        #return result.deleted_count > 0
        book=self.get_book(book_id)
        if book:
            if os.path.exists(book.file_path):
                os.remove(book.file_path)
            if book.cover_path and os.path.exists(book.cover_path):
                os.remove(book.cover_path)
            return self.books.delete_one({'_id': ObjectId(book_id)})
        return False



    
