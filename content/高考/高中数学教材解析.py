import streamlit as st



chapter1=r"F:\streamlit_kltree\streamlit_kltree\高一上册第一章.md"
def read_markdown_file(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        return f.read()

# 显示 MD 内容


st.title('高中数学')

# 侧边栏用于选择具体主题
topic = st.selectbox(
    "选择年级",
    ["高一上册", "高一下册", "高二上册"]
)

if topic == "高一上册":
    
    tab1, tab2, tab3 = st.tabs(["第一章", "第二章", "第三章"])

    with tab1:
        markdown_text = read_markdown_file(chapter1)
        st.markdown(markdown_text,unsafe_allow_html=True)
        #    st.write("展示第一章内容...")

elif topic == "高一下册":
    st.header("导数")
    st.latex(r'''f'(x) = \lim_{h \to 0}\frac{f(x+h)-f(x)}{h}''')