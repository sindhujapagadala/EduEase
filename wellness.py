import streamlit as st
import time
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API globally
genai.configure(api_key=GEMINI_API_KEY)

def counsellor():
    persist_directory = 'wellness_cur/chroma'

    # Use local HuggingFace embeddings instead of OpenAI embeddings
    # (Gemini does not directly provide vector embeddings API yet in LangChain)
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load or create vector database
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

    st.markdown(
        '<i><h3 style="font-family:Arial;color:#1F2839;text-align:center;'
        'font-size:20px;padding-left:50px">'
        'AI-powered support for your mental wellness — start a chat now</h3><i>',
        unsafe_allow_html=True
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous chat history
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

            # Retrieve relevant docs
            retriever = vectordb.as_retriever()
            docs = retriever.get_relevant_documents(prompt)
            context = "\n".join([doc.page_content for doc in docs])

            # Create prompt
            template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, try to make up an answer but keep it related to the topic. 
Use three sentences maximum. Ask clarifying questions to better understand the problem. 
Be empathetic and understanding — you are dealing with teachers who want counselling.  

Context:
{context}

Question: {question}

Helpful Answer:"""

            QA_CHAIN_PROMPT = PromptTemplate(
                input_variables=["context", "question"],
                template=template
            )

            # Fill the template
            final_prompt = QA_CHAIN_PROMPT.format(context=context, question=prompt)

            # Call Gemini for response
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(final_prompt)

            # Simulate streaming effect
            full_response += response.text
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.05)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    counsellor()
