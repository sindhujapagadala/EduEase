import streamlit as st
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

def run_summary(llm, retriever):
    """Helper to run the summary query with a given LLM."""
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

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )

    return qa_chain({
        "query": "Summarize this lesson for me. I am a teacher, I need to better understand this lesson. Put it in bullet points."
    })

def summarize():
    uploaded_file = st.file_uploader("Upload PDF File Of Your Lesson", type="pdf")

    if uploaded_file:
        with st.spinner("Summarizing lesson into bullet points..."):
            with open(uploaded_file.name, mode='wb') as w:
                w.write(uploaded_file.getvalue())

            loader = PyPDFLoader(uploaded_file.name)
            pages = loader.load()

            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150
            )
            splits = text_splitter.split_documents(pages)

            try:
                asyncio.get_running_loop()
            except RuntimeError:
                asyncio.set_event_loop(asyncio.new_event_loop())

            embedding = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=GEMINI_API_KEY
            )

            persist_directory = 'docs/chroma/'
            vectordb = Chroma.from_documents(
                documents=splits,
                embedding=embedding,
                persist_directory=persist_directory
            )

            llm_pro = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                temperature=0,
                google_api_key=GEMINI_API_KEY
            )

            try:
                result = run_summary(llm_pro, vectordb.as_retriever())
            except Exception as e:
                if "429" in str(e):
                    llm_flash = ChatGoogleGenerativeAI(
                        model="gemini-1.5-flash",
                        temperature=0,
                        google_api_key=GEMINI_API_KEY
                    )
                    result = run_summary(llm_flash, vectordb.as_retriever())
                else:
                    st.error(f"Error generating summary: {e}")
                    vectordb.delete_collection()
                    return

            summary_text = result.get("result", "").strip()

            if summary_text:
                st.markdown("### 📌 Lesson Summary")
                st.markdown(summary_text)
            else:
                st.error("No summary generated from the model.")

            vectordb.delete_collection()
            st.info("Lesson summarized successfully!")
