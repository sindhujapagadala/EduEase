import streamlit as st
import pandas as pd
import google.generativeai as genai

import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Access the keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def query_chatgpt(prompt):
    return "Response from ChatGPT"

# Function to query Gemini API with a specific question and dataset context
def query_gemini(question, context):
    prompt = f"""
    Given the following dataset:
    {context}

    Answer the following question concisely and write your final calculation:
    {question}
    """

    prompt2 = """You are a teacher who excels in statistics. 
    After receiving the data, you have to do calculations and answer the query 
    asked by the user. You are the best in analyzing data in the whole world.
    You do not have to show how you are calculating the answers."""

    model = genai.GenerativeModel("gemini-pro")

    response = model.generate_content([{"role": "system", "content": prompt2}, 
                                       {"role": "user", "content": prompt}])

    return response.text

# Streamlit app
upload_file = st.file_uploader("Upload CSV file with student data", type="csv")

if upload_file is not None:
    # Load the data
    df = pd.read_csv(upload_file)

    # Display the dataframe
    st.write("### Uploaded Data", df)

    # Ask the teacher to input a question
    question = st.text_area("Ask a question about the dataset:")

    if st.button("Get Answer"):
        # Convert dataframe to a string format
        context = df.to_string(index=False)

        # Query Gemini
        answer = query_gemini(question, context)

        # Display the answer
        st.write("### Answer from Gemini")
        st.write(answer)