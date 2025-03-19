import streamlit as st
import time
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings  # Keeping OpenAI embeddings

import os
from dotenv import load_dotenv


# Load API keys from .env
load_dotenv()

# Access the keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def summarize():
    uploaded_file = st.file_uploader("Upload PDF File Of Your Lesson")

    if uploaded_file:
        with st.spinner("Summarizing lesson into bullet points..."):
            with open(uploaded_file.name, mode='wb') as w:
                w.write(uploaded_file.getvalue())
            loader = PyPDFLoader(uploaded_file.name)
            pages = loader.load()
            
            # Split
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150
            )

            splits = text_splitter.split_documents(pages)

            # Using OpenAI embeddings
            embedding = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

            persist_directory = 'docs/chroma/'

            vectordb = Chroma.from_documents(
                documents=splits,
                embedding=embedding,
                persist_directory=persist_directory
            )

            template = """Use the following pieces of context and summarize the whole lesson for the teacher in bullet points to help teachers understand the lesson. Keep the answer concise.
            {context}
            Question: {question}
            Helpful Answer:"""

            QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

            # Retrieve context from vector database
            retriever = vectordb.as_retriever()
            retrieved_docs = retriever.get_relevant_documents("Summarize this lesson for me in bullet points.")

            context = "\n".join([doc.page_content for doc in retrieved_docs])

            prompt = template.format(context=context, question="Summarize this lesson in bullet points.")

            # Generate response using Gemini API
            model = genai.GenerativeModel("gemini-pro")
            response = model.generate_content(prompt)

            st.success(response.text)

            vectordb.delete_collection()
