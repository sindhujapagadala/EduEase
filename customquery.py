import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def query_gemini(question, context):
    """
    Sends a question and dataset context to Gemini and returns the answer.
    """
    prompt2 = """You are a teacher who excels in statistics.
After receiving the data you have to do calculations and answer the query 
asked by the user. You are the best in analyzing data in the whole world.
You do not have to show how you are calculating the answers."""

    final_prompt = f"""{prompt2}

Given the following dataset:
{context}

Answer the following question concisely and write your final calculation:
{question}
"""

    model = genai.GenerativeModel("gemini-1.5-pro") 
    response = model.generate_content(final_prompt)

    return response.text.strip()

st.title("EduEase - Dataset Query with Gemini AI")

uploaded_file = st.file_uploader("Upload CSV file with student data", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.write("### Uploaded Data", df)
    question = st.text_area("Ask a question about the dataset:")

    if st.button("Get Answer"):

        context = df.to_string(index=False)

        answer = query_gemini(question, context)

        st.write("### Answer from Gemini")
        st.write(answer)
