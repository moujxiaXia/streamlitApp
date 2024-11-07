# -*- coding: utf-8 -*-
"""
Created on 2024-11-07

@author: Administrator
"""
import streamlit as st
import time
import openai

# 设置你的OpenAI API密钥
openai.api_key = st.secrets["TOKEN"] 

# Password protection
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.text_input(
            "请输入密码", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input(
            "请输入密码", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 密码错误")
        return False
    else:
        # Password correct
        return True

if not check_password():
    st.stop()  # Do not continue if check_password is False

# 页面标题
st.title("Chat-O4 模型对话助手")

# 在侧边栏设置选项
st.sidebar.title("设置选项")
model = st.sidebar.selectbox("选择模型", ["gpt-3.5-turbo", "gpt-4"])
temperature = st.sidebar.slider("选择Temperature", 0.0, 1.0, 0.7)

# 用于记录对话的 session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 开始新的会话按钮
if st.sidebar.button("开始新会话"):
    st.session_state.messages = []
    st.success("已创建新会话")

# 用户输入
user_input = st.text_input("请输入您的问题：")

# 显示对话输出
if user_input:
    # 将用户输入加入到对话历史中
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 调用 OpenAI API 获取回复
    response = openai.ChatCompletion.create(
        model=model,
        messages=st.session_state.messages,
        temperature=temperature,
    )

    # 获取回复内容并显示
    assistant_reply = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.write("**Assistant**:", assistant_reply)

# 显示完整对话记录
st.subheader("对话记录")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write("**You**:", msg["content"])
    else:
        st.write("**Assistant**:", msg["content"])

