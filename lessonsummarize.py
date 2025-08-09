import streamlit as st
import time
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Access Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def summarize():
    uploaded_file = st.file_uploader("Upload PDF File Of Your Lesson", type="pdf")

    if uploaded_file:
        with st.spinner("Summarizing lesson into bullet points..."):
            # Save uploaded file temporarily
            with open(uploaded_file.name, mode='wb') as w:
                w.write(uploaded_file.getvalue())

            # Load PDF pages
            loader = PyPDFLoader(uploaded_file.name)
            pages = loader.load()

            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150
            )
            splits = text_splitter.split_documents(pages)

            # Use Gemini embeddings
            embedding = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=GEMINI_API_KEY
            )

            persist_directory = 'docs/chroma/'

            # Create Chroma vector database
            vectordb = Chroma.from_documents(
                documents=splits,
                embedding=embedding,
                persist_directory=persist_directory
            )

            # Use Gemini for retrieval QA
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",  # or gemini-1.5-flash
                temperature=0,
                google_api_key=GEMINI_API_KEY
            )

            # Prompt template
            template = """Use the following context to summarize the lesson for a teacher.
Provide bullet points only, keeping the answer concise.  
If you don't know the answer, say you don't know.  

Context:
{context}

Question: {question}

Helpful Answer:"""

            QA_CHAIN_PROMPT = PromptTemplate(
                input_variables=["context", "question"],
                template=template
            )

            # Create RetrievalQA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm,
                retriever=vectordb.as_retriever(),
                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
            )

            # Run query
            result = qa_chain({
                "query": "Summarize this lesson for me. I am a teacher, I need to better understand this lesson. Put it in bullet points."
            })

            st.success(result['result'])

            # Clean up database
            vectordb.delete_collection()
            st.success("Lesson summarized successfully!")