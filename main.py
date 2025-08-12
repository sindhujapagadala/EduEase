import streamlit as st
import sys
import os
from teacheranalysis import analysis
from MCQ import MCQ
from LessonPlan import lessonplan
from lessonsummarize import summarize
from wellness import counsellor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(
    page_title="Your Smart Teaching Companion",
    page_icon=":teacher:",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        /* Force Sans-serif everywhere */
        html, body, .stApp, [class^="css"], [class*="css"], 
        div, p, span, label, h1, h2, h3, h4, h5, h6, 
        button, input, textarea, select {
            font-family: 'Sans-serif' !important;
        }

        /* App background */
        .stApp {
            background-color: #FFE3C7; /* Soft peach background */
            color: #000000;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #f8a853ff; /* Orange sidebar */
        }

        /* Keep sidebar selectbox default style */
        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: white !important;
            color: black !important;
            border-radius: 6px !important;
        }
        section[data-testid="stSidebar"] div[data-baseweb="select"] * {
            color: black !important;
        }

        /* Primary buttons */
        div.stButton > button {
            background-color: #f57c00;
            color: white;
            border: none;
            border-radius: 6px;
        }
        div.stButton > button:hover {
            background-color: #e76f00;
        }

        /* Headers and text */
        h1, h2, h3, h4, h5, h6 {
            color: #000000;
        }
        p, span, label {
            color: #000000;
        }

        /* File uploader styling */
        [data-testid="stFileUploader"] {
            background-color: #FFD2A0 !important;
            border-radius: 8px !important;
            padding: 1em !important;
        }
        [data-testid="stFileUploader"] > div {
            background-color: #FFD2A0 !important;
            border-radius: 8px !important;
        }
        [data-testid="stFileUploaderDropzone"] {
            background-color: #FFE3C7 !important;
            border: 2px dashed #f57c00 !important;
        }
        [data-testid="stFileUploader"] span,
        [data-testid="stFileUploader"] p {
            color: #000000 !important;
        }
        [data-testid="stFileUploader"] button {
            background-color: #f57c00 !important;
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
        }
        [data-testid="stFileUploader"] button:hover {
            background-color: #e76f00 !important;
        }

        /* Alerts */
        .stAlert {
            background-color: #FFD2A0 !important;
            color: #000000 !important;
        }

        /* Dataframes / tables */
        .stDataFrame {
            background-color: #FFF2E0;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #FFD2A0;
            color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='text-align:center; font-size:3rem; font-family:Sans-serif; color:#000000;'>Your Smart Teaching Companion</h1>",
    unsafe_allow_html=True
)

options = st.sidebar.selectbox(
    "How May I Assist?",
    [
        "🧑‍🏫 Perform Analysis",
        "📝 Generate Quiz",
        "📋 Generate Lesson Plan",
        "📄 Summarize Lesson",
        "💡 Virtual AI Counsellor"
    ]
)

if options == "🧑‍🏫 Perform Analysis":
    analysis()
elif options == "📝 Generate Quiz":
    MCQ()
elif options == "📋 Generate Lesson Plan":
    lessonplan()
elif options == "📄 Summarize Lesson":
    summarize()
elif options == "💡 Virtual AI Counsellor":
    counsellor()

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
