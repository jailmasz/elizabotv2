import os
import streamlit as st
from langflow import load_flow_from_json
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")

flow = load_flow_from_json("flow/elizabot.json")


def add_bg_from_url():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://cdn.pixabay.com/photo/2023/02/06/18/30/ai-generated-7772547_640.jpg");
            background-attachment: fixed;
            background-size: cover;
            min-height: 100vh;
        }
        @media (max-width: 768px) {
            .stApp {
                background-size: cover;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Eliza Bot", page_icon="🤖")
    add_bg_from_url()
    st.title("Eliza Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    with st.container():
        st.markdown(
            """
            <style>
            .stChatFloatingInputContainer {
                background-image: url("https://cdn.pixabay.com/photo/2023/02/06/18/30/ai-generated-7772547_640.jpg");
                background-attachment: fixed;
                background-size: cover;
                padding: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        prompt = st.chat_input(
            "Oi, Sou a Eliza Bot, sua psicóloga virtual. Como você está se sentindo hoje?"
        )

        if prompt:
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
            })

            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner(text="Digitando..."):
                    user_input = {"text": prompt}
                    response = flow(user_input)
                    answer = response["text"]
                    message_placeholder.write(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
            })


if __name__ == "__main__":
    main()
