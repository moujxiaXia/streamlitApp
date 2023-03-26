# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 19:58:44 2023

@author: Administrator
"""
import openai
import streamlit as st

openai.api_key = st.secrets["TOKEN"] 
#用来生成图像的文本提示

def create_image():
    response=openai.Image.create(prompt=st.session_state.input_txt,
                  n=1,
                  model="image-alpha-001",
                  size=st.session_state.image_size,
                  response_format="url") 

    #第一张图片
    st.session_state.url=response["data"][0]["url"]
    
if 'input_txt' not in st.session_state:
    st.session_state.input_txt = ""
    st.session_state.image_size = "512x512"
    st.session_state.url = ""
    
with st.form(key='my_form'):
    st.selectbox(
    'Image size:',
    ("256x256", "512x512", "1024x1024"), key='image_size')

    st.text_input('Enter the prompt', "", key='input_txt')
    submit = st.form_submit_button(label='Create', on_click=create_image)


if st.session_state.url:
    st.image(st.session_state.url)
