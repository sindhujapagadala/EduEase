import streamlit as st
import time
import langchain
import openai
import google.generativeai as genai
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Access the keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
def counsellor():
    

    openai_key = OPENAI_API_KEY

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
    genai.configure(api_key=GEMINI_API_KEY)


    persist_directory = 'wellness_cur/chroma'

    embedding = OpenAIEmbeddings(api_key=openai_key)

    vectordb = Chroma(persist_directory=persist_directory,embedding_function=embedding)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key = openai_key)


    # st.markdown('<h1 style="font-family:Times New Roman;color:darkred;text-align:center;">AI Counsellor For Mental Wellness</h1>',unsafe_allow_html=True)
    st.markdown('<i><h3 style="font-family:Arial;color:#1F2839;text-align:center;font-size:20px;padding-left:50px">AI-powered support for your mental wellness—start a chat now</h3><i>',unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # Accept user input
    if prompt := st.chat_input("How may I help you!"):
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)


    # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, try to make up an answer but related to topic. Use three sentences maximum. Ask questions to get more better understanding of the problem. Be empathetic, understanding as you are dealing with teachers who want counselling.  
            {context}
            Question: {question}
            Helpful Answer:"""
            QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"],template=template)

            # Run chain
            qa_chain = RetrievalQA.from_chain_type(
                llm,
                retriever=vectordb.as_retriever(),
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
            )
            
            model = genai.GenerativeModel("gemini-2.0-flash")
            result = qa_chain({"query": prompt})

            # Simulate stream of response with milliseconds delay
            full_response += result["result"]
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history

        st.session_state.messages.append({"role": "assistant", "content": full_response})