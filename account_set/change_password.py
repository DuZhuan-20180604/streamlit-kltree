import streamlit as st
from auth import Auth

if st.session_state.user:
    with st.form("修改密码"):
        st.subheader("修改密码")
        old_password = st.text_input("旧密码", type="password")
        new_password = st.text_input("新密码", type="password")
        confirm_password = st.text_input("确认新密码", type="password")
        
        if st.form_submit_button("更新密码"):
            if not all([old_password, new_password, confirm_password]):
                st.error("请填写所有字段")
            elif new_password != confirm_password:
                st.error("两次密码不一致")
            else:
                success, message = Auth.update_password(
                        st.session_state.user['_id'],
                        old_password,
                        new_password
                    )
                if success:
                    st.success(message)
                else:
                    st.error(message)