
import streamlit as st
#from auth import Auth
st.set_page_config(
    page_title="知识学习树",
    page_icon="🌲",
    layout="wide",
    initial_sidebar_state="expanded"
)

#st.write(st.session_state)
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role=None

main_page=st.Page("home_page/home.py",title="主页",icon=":material/home:",default=True)

login_page=st.Page("account/login.py",title="登录",icon=":material/login:")
register_page=st.Page("account/register.py",title="注册",icon=":material/assignment:")

zk_tb_page=st.Page("content/中考/初中数学教材解析.py",title="初中数学教材解析",icon=":material/book:")
gk_tb_page=st.Page("content/高考/高中数学教材解析.py",title="高中数学教材解析",icon=":material/book:")
ky_tb_page=st.Page("content/考研/考研数学教材解析.py",title="考研数学教材解析",icon=":material/book:")

zk_exam_page=st.Page("content/中考/中考真题解析.py",title="中考真题解析",icon=":material/note:")
gk_exam_page=st.Page("content/高考/高考真题解析.py",title="高考真题解析",icon=":material/note:")
ky_exam_page=st.Page("content/考研/考研真题解析.py",title="考研真题解析",icon=":material/note:")

book_download_page=st.Page("download/电子书下载.py",title="电子书下载",icon=":material/download:")

flow_page=st.Page("tools/流程图.py",title="流程图")

change_password_page=st.Page("account_set/change_password.py",title="修改密码",icon=":material/lock:")
delete_account_page=st.Page("account_set/delete_account.py",title="注销账号",icon=":material/delete:")

account_pages=[login_page,register_page]

settings_pages=[change_password_page,delete_account_page]

zk_tb_pages=[zk_tb_page]
gk_tb_pages=[gk_tb_page]
ky_tb_pages=[ky_tb_page]

zk_exam_pages=[zk_exam_page]
gk_exam_pages=[gk_exam_page]
ky_exam_pages=[ky_exam_page]

zk_pages=[zk_tb_page,zk_exam_page]
gk_pages=[gk_tb_page,gk_exam_page]
ky_pages=[ky_tb_page,ky_exam_page]

tool_pages=[flow_page]

download_pages=[book_download_page]

pages_dict={}



if st.session_state.role in [None]:
    pages_dict["主页"]=[main_page]
    pages_dict["账号"]=account_pages
    pages_dict["中考"]=zk_tb_pages
    pages_dict["高考"]=gk_tb_pages
    pages_dict["考研"]=ky_tb_pages
    pages_dict["下载专区"]=download_pages
    pages_dict["工具"]=tool_pages
if st.session_state.role in ["USER","user"]: 
    pages_dict["主页"]=[main_page]   
    pages_dict["中考"]=zk_pages
    pages_dict["高考"]=gk_pages
    pages_dict["考研"]=ky_pages
    pages_dict["下载专区"]=download_pages
    pages_dict["工具"]=tool_pages
    pages_dict["账号管理"]=settings_pages

with st.sidebar:
    if st.session_state.user or st.session_state.role !=None:
        if st.button("🚪 退出登录",):
            st.session_state.user=None
            st.session_state.role=None
            st.rerun()

pg=st.navigation(pages_dict) 
pg.run()

print(st.session_state)






