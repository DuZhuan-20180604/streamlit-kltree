import streamlit as st
#from auth import Auth
from db_users import UserManager

user_manager = UserManager()
def show_password_reset_ui():
    st.subheader("重置密码")

    with st.form("reset_password_form"):
        email = st.text_input("请输入注册邮箱")
        reset_code = st.text_input("验证码")
        new_password = st.text_input("新密码", type="password")
        confirm_password = st.text_input("确认新密码", type="password")
        if st.form_submit_button("获取验证码"):
            if email:
                success, message = user_manager.request_password_reset(email)
                print(success, message) 
                if success:
                    st.session_state.reset_email = email
                    
                    st.success(f"验证码已发送（测试阶段显示）：{message}")
                    st.rerun()
                else:
                    
                    st.error(message)
            else:
                st.error("请输入邮箱")
        if st.form_submit_button("重置密码"):
            if not all([reset_code, new_password, confirm_password]):
                st.error("请填写所有字段")
            elif new_password != confirm_password:
                st.error("两次密码不一致")
            else:
                success, message = user_manager.reset_password(
                    st.session_state.reset_email,
                    reset_code,
                    new_password
                )
                if success:
                    st.success(message)
                    # 清除重置状态
                    
                    del st.session_state.reset_email
                    st.session_state.show_reset = False
                    st.rerun()
                else:
                    st.error(message)
    
    # 返回按钮
    if st.button("返回"):
        del st.session_state.reset_step
        st.session_state.show_reset = False
        st.rerun()

def show_login_ui():
    if hasattr(st.session_state, 'show_reset') and st.session_state.show_reset:
        show_password_reset_ui()
    else:
        with st.form("login_form"):
            identifier = st.text_input("用户名/邮箱/ID")
            password = st.text_input("密码", type="password")

            col1, col2 ,col3= st.columns(3)
            with col1:
                submit = st.form_submit_button("登录")
            with col2:
                if st.form_submit_button("忘记密码?"):
                    st.session_state.show_reset = True
                    #st.session_state.reset_step = 1
                    st.rerun()
            with col3:
                st.warning('没有账号？请到注册页注册!', icon="⚠️")

            if submit:
                success, user = user_manager.login(identifier, password)
                print("b:",success, user)
                if success:
                    st.session_state.user = user
                    st.session_state.role = user['role']
                 
                    st.success("登录成功！")
                    st.rerun()
                else:
                    st.error("登录失败，请检查用户名和密码")



show_login_ui()






