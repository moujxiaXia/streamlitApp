# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 23:04:53 2023

@author: Administrator
"""

import streamlit as st
import requests

# Your OpenAI API Key
api_key = st.secrets["TOKEN"] 

u = 'https://api.openai.com/v1/chat/completions'
# The headers for the API request
h = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


class ChatGPT:  
    def __init__(self,chat_list=[]) -> None:  
        # 初始化对话列表  
        self.chat_list = []  
  
    
      
    # 显示接口返回  
    def show_conversation(self):  
        msg_list = self.chat_list
        msgAll = ""
        for msg in msg_list:  
            if msg['role'] == 'user':  
                msgAll += f"user: {msg['content']}\n"
                #print(f"Me: {msg['content']}\n")  
            else:  
                msgAll += f"assistant: {msg['content']}\n"
                #print(f"ChatGPT: {msg['content']}\n")  
        return msgAll
  
    # 提示chatgpt  
    def ask(self,prompt):  
        self.chat_list.append({"role":"user","content":prompt}) 
        allmsg = self.show_conversation()
        d = {
            "model": "gpt-3.5-turbo-0613",
            "messages": [{"role": "user", "content":allmsg}],
            "temperature": 0.7
         }

        response = requests.post(u, headers=h, json=d)
        #response = openai.ChatCompletion.create(model="gpt-3.5-turbo",messages=self.chat_list)  
        answer = response.json()["choices"][0]["message"]["content"]
        # 添加历史对话，形成上下文关系  
        self.chat_list.append({"role":"assistant","content":answer})  
        #self.show_conversation(self.chat_list)  

col1, col2 = st.columns(2)  #([1, 3])
# Initialization
if 'chat' not in st.session_state:
    st.session_state.chat = ChatGPT()
    st.session_state.input_text = ""

# the callback function for the button will add 1 to the
# slider value up to 10
def asktochat():
    st.session_state.chat.ask(st.session_state.input_text)


with col1:
    with st.form(key='my_form'):
        st.text_input("输入文本栏", "", key='input_text')
        submit = st.form_submit_button(label='Send', on_click=asktochat)

with col2:
    st.button("Clear")
    outtext = st.session_state.chat.show_conversation()
    st.text_area("history", outtext, height=600)

