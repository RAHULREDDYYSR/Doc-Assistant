from typing import Set
import streamlit as st
from backend.core import run_llm

# Page config
st.set_page_config(
    page_title="Documentation Helper",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
    }
    .css-1d391kg {
        background-color: #161b22;
    }
    .stButton>button {
        background-color: #238636;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 6px 16px;
    }
    .stTextInput>div>div>input {
        background-color: #161b22;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 6px;
    }
    .stMarkdown {
        color: #c9d1d9;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar user information
with st.sidebar:
    st.title("User Profile")
    # Add profile picture with rounded corners
    st.markdown("""
        <style>
        .profile-img {
            border-radius: 50%;
            border: 2px solid #30363d;
        }
        </style>
        """, unsafe_allow_html=True)
    st.image("https://www.w3schools.com/howto/img_avatar.png", width=150, output_format="auto")
    
    # Add user information
    user_name = st.text_input("Name", placeholder="Enter your name")
    user_email = st.text_input("Email", placeholder="Enter your email")
    
    if user_name and user_email:
        st.success(f"Welcome {user_name}!")
        st.write(f"📧 {user_email}")
    
    st.divider()

# Main content
st.markdown("<h1 style='color: #c9d1d9;'>Langchain Documentation Helper bot</h1>", unsafe_allow_html=True)

prompt = st.text_input("Ask me anything...", placeholder="Enter your prompt here...", help="Type your question and press Enter")

if (
    "chat_answer_history" not in st.session_state
    and "user_prompt_history" not in st.session_state
    and "chat_history" not in st.session_state
):
    st.session_state["user_prompt_history"] = []
    st.session_state["chat_answer_history"] = []
    st.session_state["chat_history"] = []


def create_sources_string(source_url: Set[str]) -> str:
    if not source_url:
        return ""
    source_list = list(source_url)
    source_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(source_list):
        sources_string += f"{i+1}. {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(
            query=prompt, chat_history=st.session_state["chat_history"]
        )
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        formatted_response = (
            f"{generated_response['result']} \n\n {create_sources_string(sources)}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_answer_history"].append(formatted_response)
        st.session_state["chat_history"].append(("human", prompt))
        st.session_state["chat_history"].append(("ai", generated_response["result"]))


if st.session_state["chat_answer_history"]:
    for generated_response, user_query in zip(
        st.session_state["chat_answer_history"], st.session_state["user_prompt_history"]
    ):
        st.chat_message("user").write(user_query)
        st.chat_message("assistant").write(generated_response)
