import streamlit as st
from PIL import Image

def show_donation():
    st.markdown("""
        <div style='text-align: center; color: #1a73e8;'>
            如果这个网站对您有帮助，欢迎扫描下方二维码赞助这个网站 
        </div>
    """, unsafe_allow_html=True)
    
    # 加载二维码图片
    qr_path = "./收款码.png"  # 替换为你的二维码图片路径
    try:
        qr_image = Image.open(qr_path)
        # 在页面中央显示二维码
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(qr_image, caption='微信赞助', width=200)
    except FileNotFoundError:
        st.warning("二维码图片未找到，请确保图片路径正确")

if st.session_state.user:
    st.markdown("""
        ### 👋 欢迎来到数学学习平台！

        #### 📚 课程内容
        - **初中数学**
            - 基础代数
            - 几何
            - 函数初步
        
        - **高中数学**
            - 函数与导数
            - 立体几何
            - 概率统计
        
        - **考研数学**
            - 高等数学
            - 线性代数
            - 概率论
        #### 💡 使用指南
        1. 选择你感兴趣的课程
        2. 按章节学习
        3. 记录笔记
        4. 追踪进度
        
        #### 🎯 学习建议
        - 循序渐进
        - 多做练习
        - 及时复习
        [![点击我](kltree/static/Leonhard_Euler.jpg.jpg)](https://www.baidu.com)
              
            """)
    show_donation()
else:
    st.warning("""👋 请先登录以访问完整功能""")
    st.markdown("""
        ### 🎓 平台特色
        
        - **📚 丰富的课程内容**
          - 初中到考研全覆盖
          - 系统化的知识体系
        
        - **🎯 个性化学习**
          - 进度追踪
          - 笔记系统
        
        - **💡 智能辅导**
          - 练习推荐
          - 重点提醒
        
        ### 🌟 立即加入
        注册账号，开启你的数学学习之旅！
        [![点击我](kltree/static/Leonhard_Euler.jpg.jpg)](https://www.baidu.com)
        """)
    show_donation()