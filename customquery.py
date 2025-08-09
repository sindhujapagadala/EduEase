import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Access the GEMINI API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Function to query Gemini with dataset context
def query_gemini(question, context):
    """
    Sends a question and dataset context to Gemini and returns the answer.
    """
    # System-like role prompt
    prompt2 = """You are a teacher who excels in statistics.
After receiving the data you have to do calculations and answer the query 
asked by the user. You are the best in analyzing data in the whole world.
You do not have to show how you are calculating the answers."""

    # Combine context + question
    final_prompt = f"""{prompt2}

Given the following dataset:
{context}

Answer the following question concisely and write your final calculation:
{question}
"""

    # Use Gemini's chat-like API
    model = genai.GenerativeModel("gemini-1.5-pro")  # or gemini-1.5-flash
    response = model.generate_content(final_prompt)

    return response.text.strip()

# -----------------------
# Streamlit App
# -----------------------

st.title("EduEase - Dataset Query with Gemini AI")

uploaded_file = st.file_uploader("Upload CSV file with student data", type="csv")

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)

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
