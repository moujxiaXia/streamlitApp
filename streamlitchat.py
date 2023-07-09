import streamlit as st
import openai

# 设置OpenAI API密钥
#openai.api_key = 'YOUR_API_KEY'
# Your OpenAI API Key
openai.api_key = st.secrets["TOKEN"]
# 定义对话函数
def chat_with_gpt(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',  # 这里使用GPT-3.5的引擎，ChatGPT 4.0使用的引擎可能不同
        prompt=prompt,
        max_tokens=50,  # 设置生成的响应长度
        n = 1, # 设置返回的响应数量
        stop=None,  # 可以设置停止标记来结束响应
        temperature=0.7,  # 调整生成响应的创造性程度
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# Streamlit应用程序
def main():
    st.title('ChatGPT Demo')

    # 获取用户输入的对话提示
    prompt = st.text_input('User Input', value='', max_chars=100)

    if st.button('Send'):
        # 与GPT对话并获取响应
        response = chat_with_gpt(prompt)

        # 显示GPT的响应
        st.text_area('ChatGPT', value=response, height=200)

# 运行Streamlit应用程序
if __name__ == '__main__':
    main()
