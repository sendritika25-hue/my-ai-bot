import streamlit as st
from groq import Groq
import PyPDF2

st.set_page_config(page_title="Nirvaan's AI Bot", page_icon="🤖")
st.title("🤖 Nirvaan's Personal AI Chatbot")
st.write("Welcome! Step into the future with my custom-engineered AI companion.")

# --- PDF Extract Function ---
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

# Seedhe Streamlit Secrets se API key uthane ke liye
if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
elif "api_key" in st.secrets:
    GROQ_API_KEY = st.secrets["api_key"]
else:
    GROQ_API_KEY = ""

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

# --- Sidebar for PDF Upload ---
with st.sidebar:
    st.header("Document Settings")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

pdf_context = ""
if uploaded_file is not None:
    pdf_context = extract_text_from_pdf(uploaded_file)
    st.sidebar.success("PDF successfully uploaded and scanned!")

# Chat history initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Purani baatein screen par dikhane ke liye
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if user_prompt := st.chat_input("Ask me anything..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Context checking (Purani chat history include karne ke liye aur PDF context add karne ke liye)
    messages_payload = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    
    # Agar PDF uploaded hai, toh aane wale message mein context jodna
    current_message_content = user_prompt
    if pdf_context:
        current_message_content = f"Context from uploaded PDF:\n{pdf_context}\n\nUser Question: {user_prompt}"
        
    messages_payload.append({"role": "user", "content": current_message_content})

    # Groq API call
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages_payload,
                stream=False
            )
            full_response = completion.choices[0].message.content
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {e}")
            
    # Save the conversation history (Original user prompt save karenge takki UI me ganda na dikhe)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.messages.append({"role": "assistant", "content": full_response})
