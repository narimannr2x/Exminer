CHROMA_PATH = "chroma"
DATA_PATH = "data"
########################################################################
#local imports
from get_response import get_response
from populate_database import load_documents, split_documents, add_to_chroma,calculate_chunk_ids, clear_database
#global imports
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
###################################################################
#function definition 
def show_messages():
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

def set_up_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello, I am a bot. How can I help you?"),
        ]

def pop_database():
    # Create (or update) the data store.
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)


###################################################################
#page title
st.set_page_config(page_title="Streaming bot", page_icon="🤖")
st.title("a simple LLM chatbot")
#########################################################################
#setting up session state
set_up_session_state()    
# conversation chain display
show_messages()
#############################################################################
# user input
user_query = st.chat_input("Type your message here...")
#################################################################################
pop_database()
#############################################################################
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        #we use get response method here
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(content=response))
###############################################################################