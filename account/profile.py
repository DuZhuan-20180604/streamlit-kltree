import streamlit as st
from PIL import Image
import os

def show_user_profile(user_data):
    st.markdown("""
        <style>
        .user-info {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 5px 0;
        }
        .icon {
            font-size: 1.2em;
            color: #1f77b4;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        # 用户基本信息
        st.markdown(f"""
            <div class="user-info">
                👤 <strong>用户名：</strong>{user_data.get('username', '未设置')}
            </div>
            <div class="user-info">
                🆔 <strong>用户ID：</strong>{user_data.get('user_id', 'N/A')}
            </div>
            <div class="user-info">
                📧 <strong>邮箱：</strong>{user_data.get('email', '未设置')}
            </div>
            <div class="user-info">
                📅 <strong>注册时间：</strong>{user_data.get('created_at', '未知')}
            </div>
            <div class="user-info">
                📱 <strong>手机：</strong>{user_data.get('phone', '未设置')}
            </div>
        """, unsafe_allow_html=True)

def show_user_profile2(user_data):
    """
    显示用户个人信息组件
    user_data: 包含用户信息的字典
    """
    st.markdown("""
        <style>
        .profile-container {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            margin: 10px 0;
        }
        .profile-header {
            font-size: 24px;
            font-weight: bold;
            color: #1f77b4;
            margin-bottom: 20px;
        }
        .info-item {
            margin: 10px 0;
            padding: 5px;
            background-color: #f0f2f6;
            border-radius: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="profile-container">', unsafe_allow_html=True)
        
        # 用户头像
        #col1, col2 = st.columns([1, 3])
        #with col1:
        #    if user_data.get('avatar'):
        #        st.image(user_data['avatar'], width=100)
        #    else:
        #        st.image("assets/images/default_avatar.png", width=100)
        #
        #with col2:
        #    st.markdown(f"### {user_data.get('username', '未设置用户名')}")
        #    st.markdown(f"**用户ID:** {user_data.get('user_id', 'N/A')}")
            
        # 用户信息列表
        st.markdown("#### 个人信息")
        st.markdown(f"""
            <div >👤 用户名: {user_data.get('username', '未设置用户名')}</div>
            <div >🆔 用户ID: {user_data.get('user_id', 'N/A')}</div>
            <div >📧 电子邮件：{user_data.get('email', '未设置')}</div>
            <div >📅 注册时间：{user_data.get('created_at', '未知')}</div>
            <div >📱 手机号码：{user_data.get('phone', '未设置')}</div>
        """, unsafe_allow_html=True)
        
        # 编辑按钮
        #if st.button("✏️ 编辑个人信息"):
        #    st.session_state.show_edit_profile = True
        
        st.markdown('</div>', unsafe_allow_html=True)

