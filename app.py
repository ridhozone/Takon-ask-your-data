import streamlit as st
from static.style import style_code
from utils_rag.chat import process_data, chat_rag


st.set_page_config(
    page_title="Takon - Ask Your Data",
    page_icon=":material/forum:",
)
st.html(style_code)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "index" not in st.session_state:
    st.session_state.index = None

if len(st.session_state.chat_history) == 0:
    with st.container(key="greeting"):
        st.title("TAKON :material/forum:")
        st.subheader("Search is Gone &mdash; Ask ON!")

for chat in st.session_state.chat_history:
    st.chat_message(chat["role"], avatar=chat["icon"]).write(chat["content"])

if st.session_state.get("pending_message", False):
    with st.spinner(":material/auto_stories: Reading data..."):
        last_user_msg = st.session_state.chat_history[-1]["content"]
        rag_response = chat_rag(last_user_msg, st.session_state.index)

    st.session_state.chat_history.append(
        {"role": "assistant", "icon": ":material/robot_2:", "content": rag_response}
    )

    st.session_state.pending_message = False
    st.rerun()


def fn_message():
    user_msg = st.session_state.chatinput
    query = user_msg.text
    files = user_msg.files

    if files:
        with st.spinner(":material/tab_search: Processing data..."):
            st.session_state.index = process_data(files)
            file_list = "\n".join(
                f"- :material/text_snippet: {file.name}" for file in files
            )
            st.session_state.chat_history.append(
                {
                    "role": "assistant",
                    "icon": ":material/robot_2:",
                    "content": f"You uploaded:\n{file_list}",
                }
            )

    if not query:
        st.toast(":material/warning: Please enter a message!")
        return

    if st.session_state.index is None:
        st.toast(":material/warning: Please upload files first!")
        return

    st.session_state.chat_history.append(
        {"role": "user", "icon": ":material/person:", "content": query}
    )

    st.session_state.pending_message = True


st.chat_input(
    key="chatinput",
    placeholder="ask...",
    accept_file="multiple",
    file_type=["pdf", "docx", "txt", "mp3"],
    on_submit=fn_message,
)
