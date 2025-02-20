import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "Welcome. Test this out plz good sir!"
)

# Model selection box
temp_model = st.selectbox("Model",options=["fast (GPT-4o mini)","standard (GPT-4o)","smart (o3 mini)"],key="temp_model",label_visibility="hidden")

if temp_model == "fast (GPT-4o mini)":
    selected_model = "gpt-4o-mini"
elif temp_model == "standard (GPT-4o)":
    selected_model = "gpt-4o"
else:
    selected_model = "o3-mini"

# Create an OpenAI client.
client = OpenAI(api_key=st.secrets["OpenAI_API_Key"])

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
        st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model=selected_model,
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
