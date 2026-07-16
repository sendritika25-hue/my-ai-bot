import streamlit as st
from groq import Groq

st.set_page_config(page_title="Nirvaan's AI Bot", page_icon="🤖")
st.title("🤖 Nirvaan's Personal AI Chatbot")
st.write("Welcome! Yeh mera khud ka banaya hua AI chatbot hai.")

# Seedhe Streamlit Secrets se API key uthane ke liye
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
elif "api_key" in st.secrets:
    GROQ_API_KEY = st.secrets["api_key"]
else:
    GROQ_API_KEY = ""

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein screen par dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input box
if user_prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # AI Response generation
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            if not GROQ_API_KEY:
                raise ValueError("API Key nahi mili!")
                
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model="llama-3.1-8b-instant",
            )
            reply = chat_completion.choices[0].message.content
            response_placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            response_placeholder.markdown(f"Ohho! Kuch error aaya hai. API key check karein. Error details: {str(e)}")
       
