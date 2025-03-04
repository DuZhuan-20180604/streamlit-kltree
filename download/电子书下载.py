import streamlit as st
import os
from pathlib import Path
import pandas as pd
from db_books import BookManager,get_default_cover
from models import Book
import base64
from streamlit_pdf_viewer import pdf_viewer

book_manager = BookManager()

def get_image_as_base64(path):
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
#img_base64 = get_image_as_base64("F:/streamlit_kltree/kltree/book_covers/Leonhard_Euler.jpg")
default_image=get_default_cover()

def create_book_card(book:Book):
    """创建书籍卡片组件"""
    card_html = f"""
    <div style="
        background-color: #9D9D9E;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin: 16px 0;
        text-align: center;
    ">
        <img src="data:image/jpeg;base64,{get_image_as_base64(book.cover_path) if book.cover_path else default_image}" width="180" height="240">
        <div style="color: #FF7F27;font-size: 1.2em; font-weight: bold; margin: 12px 0;">{book.title}</div>
        <div style="color: #666; font-style: italic; margin-bottom: 8px;">作者：{book.author}</div>
        <div style="color": #507F80;"background-color: #e9ecef; padding: 4px 8px; border-radius: 12px; display: inline-block; margin-bottom: 12px;">
        分类：{book.category}
    </div>

"""
    st.markdown(card_html, unsafe_allow_html=True)

    
def create_bbook_card(book:Book):
    """创建书籍卡片组件"""
    
    
    with st.container(border=True):
        # 显示封面
        if book.cover_path:
            st.image(book.cover_path,use_container_width=True)
        else:
            st.image(get_default_cover(),width=150,use_container_width=True)
        
        # 显示书籍信息（使用 div 包装以应用居中样式）
        st.markdown(f'<div class="book-title">{book.title}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="book-author">作者：{book.author}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="book-category">分类：{book.category}</div>', unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    with col1:
        with open(book.file_path, 'rb') as file:
            st.download_button(
                label="下载",
                data=file,
                file_name=book.title + '.pdf',
                mime='application/pdf',
            )
    with col2:
        if st.button("预览"):
            st.info("预览功能暂未开放")
        
@st.dialog(title="预览",width="large")
def book_preview_dialog(book):

    with st.spinner("正在加载预览..."):
        pdf_viewer(
            book.file_path, 
            height=800,
            pages_to_render=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
            render_text=True
            )
        st.warning("想看完整内容？请下载后查看")


def create_book_manager():

    upload_dir = Path("uploads")
    covers_dir = Path("book_covers")
    upload_dir.mkdir(exist_ok=True)
    covers_dir.mkdir(exist_ok=True)

    BOOKS_PER_ROW = 6
    
    with st.sidebar:
        st.header("📤上传新书")
        with st.form("upload_form"):
            title=st.text_input("书名")
            author=st.text_input("作者")
            category=st.selectbox(
                    "分类",
                    ["初中", "高中", "大学", "其他"]
                )
            book_file = st.file_uploader(
                "选择电子书文件",
                type=['pdf'],
                help="上传PDF文件",
                )
            cover_file = st.file_uploader(
                "选择封面文件",
                type=['png','jpg','jpeg'],
                help="上传封面文件",
                )
            if st.form_submit_button("上传"):
                if all([title, author, category, book_file]):
                    success, message =book_manager.add_book(
                        title,
                        author,
                        category,
                        book_file,
                        cover_file,
                        #uploader_id=st.session_state.user['user_id']
                    )
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("请填写所有必填字段")

    col1,col2=st.columns([3,1])
    with col1:
        search_term=st.text_input("🔍 搜索")
    with col2:
        category=st.selectbox(
                "分类",
                ["全部","初中", "高中", "大学", "其他"]
            )
    books=(
        book_manager.search_books(search_term) if search_term 
        else book_manager.get_books(category if category!="全部" else None)
    )
    cols_per_row=BOOKS_PER_ROW
    for i in range(0, len(books), cols_per_row):
        cols=st.columns(cols_per_row)
        for j,col in enumerate(cols):
            if i+j < len(books):
                book=books[i+j]
                with col:
                    create_book_card(book)
                    col1, col2= st.columns(2)
                    with col1:
                        with open(book.file_path, 'rb') as file:
                            st.download_button(
                                label="下载",
                                data=file,
                                file_name=book.title +str(i)+str(j) +'.pdf',
                                mime='application/pdf',
                            )
                    with col2:
                        if st.button("预览",key=book.id):
                            #book_preview_dialog()
                            #pdf_viewer(book.file_path)
                            book_preview_dialog(book)
                    
              
create_book_manager()


        