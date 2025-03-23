import streamlit as st
import sys
import os
from teacheranalysis import analysis
from MCQ import MCQ
from LessonPlan import lessonplan
from lessonsummarize import summarize
from wellness import counsellor
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(_file_), '..')))
st.set_page_config(page_title="Your Smart Teaching Companion", page_icon=":teacher:", layout="centered")

st.markdown("<h1 style='text-align:center;font-family:Garamond,serif;color:#17252A;'>Your Smart Teaching Companion</h1>", unsafe_allow_html=True)

st.write("""
<style>
    /* Primary color */
   .stApp {
        background-color: #D3D9D4; /* Light gray background */
    }
    
   .stButton:hover,.stDropdown:hover {
         /* Darker greenish-blue on hover */
    }
    
   /* Accent color */
  .stAlert {
        background-color: ##F5B7B1; /* Yellow-orange alert color */
        color: #E74C3C; /* Reddish-orange font color */
    }
    
    /* Text colors */
   .stText {
        color: #212F3C; /* Dark gray text color */
    }
    
   .stHeader {
        color: #212F3C; /* Medium gray header color */
    }
    
   .stMarkdown {
        color: #444; /* Darker gray markdown color */
    }
         
   .stSidebar {
        background-color: #1F2839;
    }   
           
   .stInfo {
        background-color: #F5B7B1;
    }
</style>
""", unsafe_allow_html=True)

options = st.sidebar.selectbox("How May I Assist?",["🧑‍🏫 Perform Analysis","📝 Generate Quiz","📋 Generate Lesson Plan","📄 Summarize Lesson","💡 Virtual AI Counsellor"])

if options == "🧑‍🏫 Perform Analysis":
    analysis()

elif options=="📝 Generate Quiz":
    MCQ()
    
elif options=="📋 Generate Lesson Plan":
    lessonplan()

elif options=="📄 Summarize Lesson":
    summarize()

elif options=="💡 Virtual AI Counsellor":
    counsellor()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)