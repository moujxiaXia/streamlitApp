import streamlit as st

import requests

# Your OpenAI API Key
api_key = st.secrets["TOKEN"]
url = 'https://api.openai.com/v1/completions'

col1, col2 = st.columns(2)

def textDavinci03():
    # The text prompt you want to generate a response
    responsetxt = ""
    with st.sidebar:
        txt = st.text_area('Input Chat', '''   ''')
        if st.button('Send'):
            prompt = txt
            # url = 'https://api.openai.com/v1/completions'
            #url = 'https://f.openaimouj.uk/v1/completions'
            # The headers for the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            params = {
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 256,
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

    with col1:
        st.write(txt)
        st.write(responsetxt)

def turbo_35():
    # The text prompt you want to generate a response
    responsetxt = ""
    with st.sidebar:
        txt = st.text_area('Input Chat', '''   ''')
        if st.button('Send'):
            prompt = txt
            #url = 'https://f.openaimouj.uk/v1/chat/completions'
            # The headers for the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            params = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }

            # Make the API request
            response = requests.post(url, headers=headers, json=params)
            # Check if the request was successful

            if response.status_code == 200:
            # Extract the generated text from the response
                responsetxt = response.json()  # ["choices"][0]
                with col1:
                    st.write(txt)
                    st.json(responsetxt)
            else:
                responsetxt = response.status_code
                with col1:
                    st.write(txt)
                    st.write(responsetxt)



def edit_text():
    # The text prompt you want to generate a response
    responsetxt = ""
    with st.sidebar:
        txt = st.text_area('Input Chat', '''   ''')
        if st.button('Send'):
            prompt = txt
            #url = 'https://f.openaimouj.uk/v1/edits'
            # The headers for the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            params = {
                "model": "text-davinci-edit-001",
                "input": "What day of the wek is it?",
                "instruction": "Fix the spelling mistakes"
            }

            # Make the API request
            response = requests.post(url, headers=headers, json=params)
            # Check if the request was successful

            if response.status_code == 200:
                # Extract the generated text from the response
                responsetxt = response.json()["choices"][0]["text"]
            else:
                responsetxt = response.status_code

    with col1:
        st.write(txt)
        st.write(responsetxt)


def image_draw():
    responsetxt = ""
    with st.sidebar:
        txt = st.text_area('Input Chat', '''   ''')
        if st.button('Send'):
            prompt = txt
            #url = 'https://f.openaimouj.uk/v1/images/generations'
            # The headers for the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            params = {
                "prompt": "A house on the beach.",
                "n": 2,
                "size": "1024x1024"
            }

            # Make the API request
            response = requests.post(url, headers=headers, json=params)
            # Check if the request was successful

            if response.status_code == 200:
                # Extract the generated text from the response
                responsetxt = response.json()["data"]
            else:
                responsetxt = response.status_code

    with col1:
        st.write(txt)
        st.write(responsetxt)



   #st.header("A dog")
   #st.image("https://static.streamlit.io/examples/dog.jpg")

page_names_to_funcs = {
    "text-davinci-003": textDavinci03,
    "turbo-3.5": turbo_35,
    "Edits": edit_text,
    "Images": image_draw
}

demo_name = st.sidebar.selectbox("Choose a module", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()






with col2:
    #with st.container():
    txt = st.text_area('Edit Text', '''     ''', height=1000)
