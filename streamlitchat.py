import streamlit as st

import requests

# 答案保存函数，把ChatGPT的回答文本，保存到日志文件中
def saveAnswer(chatText):
    filename = f'ChatGPT_Answer.log'
    with open(filename, 'a+') as f:
        f.write(chatText)
        f.write("\n")

# Your OpenAI API Key
api_key = st.secrets["TOKEN"]
# The text prompt you want to generate a response
responsetxt = ""
with st.sidebar:
    txt = st.text_area('Input Chat', '''   ''')
    if st.button('Send'):
        prompt = txt
        url = 'https://api.openai.com/v1/completions'
        #url = 'https://f.openaimouj.uk/v1/completions'
        # The headers for the API request
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
        }
        params ={
        "model": "text-davinci-003",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=params)
        # Check if the request was successful

        if response.status_code == 200:
            # Extract the generated text from the response
            responsetxt = response.json()["choices"][0]["text"]
        else:
            responsetxt = response.status_code

st.write(txt)
#saveAnswer(txt)
st.write(responsetxt)
#saveAnswer(responsetxt)
#st.markdown(responsetxt)
