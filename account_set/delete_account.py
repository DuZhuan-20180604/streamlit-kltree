import streamlit as st
from auth import Auth

if st.session_state.user:
    with st.form("注销账号"):
        st.subheader("注销账号")
        st.warning("⚠️ 注销账号后将无法恢复！")
        confirm_password=st.text_input(
            "输入密码以确认注销",
            type="password",
            key="delete_confirm"
        )
        if st.form_submit_button("注销账号",type="secondary"):
            success, message = Auth.delete_account(
                st.session_state.user['_id'], 
                confirm_password
            )
            if success:
                st.session_state.user = None
                st.session_state.role = None 
                st.success(message)
                st.rerun()
            else:
                st.error(message)