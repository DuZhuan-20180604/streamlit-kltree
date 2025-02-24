import streamlit as st

if 'user' not in st.session_state or not st.session_state.user:
    st.warning("请先登录")
    st.stop()

st.title('初中数学')

# 使用选项卡组织内容
tab1, tab2, tab3 = st.tabs(["代数", "几何", "练习题"])

with tab1:
    st.header("代数基础")
    st.write("这里是代数内容...")
    if st.button("开始学习代数"):
        st.write("展示代数课程内容...")

with tab2:
    st.header("几何基础")
    st.write("这里是几何内容...")

with tab3:
    st.header("练习题")
    st.write("来做些练习吧！")