import streamlit as st

st.title('考研数学')

# 使用 expander 组织内容
with st.expander("高等数学"):
    st.write("微积分、级数...")
    st.latex(r'\int_a^b f(x)dx')

with st.expander("线性代数"):
    st.write("矩阵、行列式...")
    st.latex(r'A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix}')

with st.expander("概率论"):
    st.write("概率分布、统计推断...")