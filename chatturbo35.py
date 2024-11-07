# -*- coding: utf-8 -*-
"""
Created on 2024-11-07

@author: Administrator
"""
import streamlit as st
import time
import openai
import json

# 设置你的OpenAI API密钥
openai.api_key = st.secrets["TOKEN"] 


# 定义要发送给ChatGPT的请求参数
def chat_with_gpt4(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 假设GPT-4模型可用
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,  # 设置响应的最大长度，根据需要调整
        temperature=0.7,  # 设置响应的随机性，可以根据需要调整
    )
    return response['choices']['message']['content']

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

# Main app
st.title("Chat-O4 对话系统")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input type selection
input_type = st.select_slider(
    "选择输入类型",
    options=["文本", "图片", "音频", "视频"]
)

# Display chat messages from history on rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# New chat button
if st.button("开始新会话"):
    st.session_state.messages = []
    st.experimental_rerun()

# Accept user input
if prompt := st.chat_input("请输入您的问题"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        #assistant_response = f"这是对您问题 '{prompt}' 的回答。"  # 这里替换为实际的API调用
        assistant_response = chat_with_gpt4(st.session_state.messages)
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

