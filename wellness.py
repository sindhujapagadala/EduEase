import streamlit as st
import time
import openai
import langchain

import google.generativeai as genai  # Import Gemini API
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def counsellor():
    openai_key = OPENAI_API_KEY

    persist_directory = 'wellness_cur/chroma'

    embedding = OpenAIEmbeddings(api_key=openai_key)

    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    st.markdown('<i><h3 style="font-family:Arial;color:darkred;text-align:center;font-size:20px;padding-left:50px">'
                'Chat with our AI Counsellor to seek help for your mental health</h3><i>', 
                unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("How may I help you!"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            template = """Use the following pieces of context to answer the question at the end. 
            If you don't know the answer, try to make up an answer but related to the topic. 
            Use three sentences maximum. Ask questions to get a better understanding of the problem. 
            Be empathetic and understanding as you are dealing with teachers who need counseling.  
            {context}
            Question: {question}
            Helpful Answer:"""
            QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

            # Run retrieval-based query
            qa_chain = RetrievalQA.from_chain_type(
                OpenAI(model_name="gpt-3.5-turbo", temperature=0, api_key=openai_key),
                retriever=vectordb.as_retriever(),
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
            )

            result = qa_chain({"query": prompt})

            # Send the retrieved response to Gemini for final processing
            gemini_prompt = f"""
            Given this retrieved context: {result['result']}
            Respond in an empathetic and supportive way to the following user query:
            {prompt}
            """
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(gemini_prompt)

            full_response += response.text
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})
