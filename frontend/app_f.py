import streamlit as st
import requests

st.title("Streamlit + Flask Demo App")


if "responses" not in st.session_state:
    st.session_state.responses = []

if "sidebar_options" not in st.session_state:
    st.session_state.sidebar_options = []

if "count" not in st.session_state:
    st.session_state.count = 1

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


tab1, tab2 = st.tabs(["📤 Upload", "📄 View"])

with tab1:
    # ---- TEXT INPUT ----
    text_input = st.text_input("Enter some text")

    # ---- NUMBER INPUT ----
    number_input = st.number_input("Enter a number", value=0)

    # ---- FILE INPUT ----
    uploaded_file = st.file_uploader("Upload a file")
    # Checkbox
    if st.checkbox("Show message"):
        st.write("Checkbox clicked!")

    count = 1
    if st.button("Send to Backend test"):
        st.session_state.sidebar_options.append(st.session_state.count)
        st.session_state.count = st.session_state.count + 1
        url = f"http://127.0.0.1:5000/item?item_id_q={number_input}&item_name={text_input}"
        payload = {"item_id_q": number_input, "item_name": text_input}
        response = requests.get(url)

        if response.status_code == 200:
            st.success("Response from backend:")
            st.session_state.responses.append(response.json())
        else:
            st.error("Failed to connect to backend")

    if st.button("file upload"):
        st.session_state.count = st.session_state.count + 1
        url = f"http://127.0.0.1:5000/item"
        payload = {"item_id_q": number_input, "item_name": text_input}
        files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
        response = requests.post(url, data=payload, files=files)

        if response.status_code == 200:
            st.success("Response from backend:")
            st.session_state.responses.append(response.json())
            st.session_state.sidebar_options.append(response.json()["saved_file"])

        else:
            st.error("Failed to connect to backend")

    if len(st.session_state.responses) != 0:
        # st.json(st.session_state.responses)
        # method 2
        for item in st.session_state.responses:
            with st.container():
                st.write(f"response from backend: {item["message"]}")

                st.divider()


with tab2:
    st.sidebar.title("Sidebar Controls")
    choice = st.sidebar.selectbox("Choose option", st.session_state.sidebar_options)

    if choice:
        url = f"http://127.0.0.1:5000/fetchdocument?file_name={choice}"
        response = requests.get(url)
        st.markdown(
            f"""
                    # Qna on *{choice}*
                    """
        )
        # st.write(response.json()["content"])
        content = response.json()["content"]

        # 👉 Preview (first 200 chars)
        preview = content[:200] + "..." if len(content) > 200 else content

        st.write(preview)

        # 👉 Expandable full content
        with st.expander("See full content"):
            st.write(content)

        # ---- CHAT DISPLAY ----
        chat_container = st.container()

        with chat_container:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"**🧑 You:** {msg['text']}")
                else:
                    st.markdown(f"**🤖 Bot:** {msg['text']}")
                st.divider()

        # ---- INPUT (always at bottom) ----
        user_input = st.chat_input("Type your question...")

        if user_input:
            # Add user message
            st.session_state.chat_history.append({"role": "user", "text": user_input})

            # 🔥 Call your backend (example)
            url = f"http://127.0.0.1:5000/ask?user_query={user_input}"
            response = requests.get(url)

            if response.status_code == 200:
                bot_reply = response.json().get("answer", "No response")

                st.session_state.chat_history.append({"role": "bot", "text": bot_reply})
            else:
                st.session_state.chat_history.append(
                    {"role": "bot", "text": "Error from backend"}
                )
            st.rerun()
