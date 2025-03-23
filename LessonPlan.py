import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

# Access the keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


def generate_lesson_plan(unit_details, session_duration, num_sessions):
    prompt = f"""
    Unit Details:
    {unit_details}

    Session Duration: {session_duration} hours
    Number of Sessions: {num_sessions}

    The lesson plan should include:
    1. Learning objectives
    2. Lesson activities and descriptions
    3. Teaching strategies to increase student engagement
    4. Assessment methods
    5. Estimated time for each section
    6. A reference URL from YouTube for the topic of that specific session
    7. Cross-verify the URLs being provided by you to ensure they are valid and working

    For each session, provide a relevant and engaging YouTube video that aligns with the topic and learning objectives. Ensure that the video is of high quality, up-to-date, and appropriate for the target audience.

    After generating the lesson plan, please double-check all the YouTube URLs to confirm they are working and accessible. If any URLs are broken or unavailable, replace them with alternative working links that cover the same topic.

    The lesson plan should be well-structured, easy to follow, and include engaging and relevant YouTube resources to enhance the learning experience.
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text


def get_motivational_content():
    prompt = "Give a motivational quote for a teacher who is nervous for a presentation."
    
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    return response.text


def lessonplan():
    # st.title("Lesson Plan Generator")

    unit_details = st.text_area("Provide details about the unit you want to teach:", height=200)
    session_duration = st.number_input("Enter the duration of each session (in hours):", min_value=1, step=1)
    num_sessions = st.number_input("Enter the number of sessions to complete the topic:", min_value=1, step=1)

    if st.button("Generate Lesson Plan"):
        if unit_details and session_duration and num_sessions:
            lesson_plan = generate_lesson_plan(unit_details, session_duration, num_sessions)
            st.header("Lesson Plan")
            st.write(lesson_plan)
            motivation = get_motivational_content()
            st.success(motivation)
        else:
            st.warning("Please provide all the required information.")
