import streamlit as st
from groq import Groq

st.set_page_config(page_title="Nirvaan's AI Bot", page_icon="🤖")
st.title("🤖 Nirvaan's Personal AI Chatbot")
st.write("Welcome! Yeh mera khud ka banaya hua AI chatbot hai.")

# Yahan par apni copy ki hui Groq API Key daalna
GROQ_API_KEY = "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"

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
if user_prompt := st.chat_input("Puchiye kuch bhi..."):
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # AI Response generation
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model="llama3-8b-8192",
            )
            reply = chat_completion.choices[0].message.content
            response_placeholder.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            response_placeholder.markdown("Ohho! Kuch error aaya hai. API key check karein.")
