import streamlit as st

from db_users import UserManager

user_manager = UserManager()

def show_register_ui():
    with st.form("register_form"):
        username = st.text_input("用户名")
        email = st.text_input("邮箱")
        password = st.text_input("密码", type="password")
        confirm_password = st.text_input("确认密码", type="password")
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("注册"):
                if not all([username, email, password, confirm_password]):
                    st.error("请填写所有字段")
                elif password != confirm_password:
                    st.error("两次密码不一致")
                else:
                    success, message = user_manager.register(username, email, password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
        with col2:
            st.info("已有账号？请到登录页登录!")
show_register_ui()