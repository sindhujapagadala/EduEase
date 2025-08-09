import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai

from docx import Document
from docx.shared import Pt
from io import BytesIO
import docx
from animations import display_cards

import os
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)


# Cache data loading function to prevent refreshing
@st.cache_data
def load_data(file):
    return pd.read_csv(file)


# Function to get improvement suggestions from Gemini
@st.cache_data
def get_suggestions(student_name, marks_data, attendance_data):
    subject_strengths = [f"{subject}: {marks} marks" for subject, marks in marks_data.items() if marks >= 60]
    subject_weaknesses = [f"{subject}: {marks} marks" for subject, marks in marks_data.items() if marks < 60]
    
    prompt = f"""
    Student Name: {student_name}
    Subject Marks: {marks_data}
    Attendance: {attendance_data}%

    As a teacher, provide personalized suggestions for this student to improve their performance (max 100 words and in bullet points):
    - Identify strengths and weaknesses based on subject marks
    - Appreciate for subjects the student performed well
    - Recommend subject-specific study strategies where the student is weak 
    - Address attendance issues if present
    - Suggestions must be specific to the student's performance
    - Suggest ways to maintain or boost motivation

    Example:
    • Murtuza shines in English and Maths! Keep up the excellent work.
    • Science needs improvement — attend more practical sessions and relate concepts to real life.
    • Maintain high focus in strong subjects to sustain performance.
    • Improve attendance to avoid missing important lessons.

    Follow this style. Max 4 bullet points.
    """

    # Use Gemini model
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip() if response and hasattr(response, 'text') else "No suggestions generated."

# Function to get class-wide improvement suggestions from Gemini
@st.cache_data
def get_class_suggestions(subject_avgs):
    prompt = f"""
    Class Subject Averages: {subject_avgs}

    As a teacher, provide brief suggestions to improve overall class performance (max 50 words and in bullet points not more than 3):
    - Identify subjects where students are struggling
    - Recommend teaching strategies to improve these subjects
    - Suggest activities or resources to help students understand difficult concepts
    - Provide general tips to maintain or boost class motivation
    """

    # Use Gemini API
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip() if response and hasattr(response, "text") else "No suggestions generated."


# Function to calculate overall performance
def calculate_performance(marks):
    return sum(marks) / len(marks)


# Function to plot bar chart for performance
def plot_performance(subjects, marks, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=subjects, y=marks, palette="coolwarm", ax=ax)
    ax.set_title(title, fontsize=16)
    ax.set_ylim(0, 100)
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', 
                    (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', 
                    xytext=(0, 9), 
                    textcoords='offset points', 
                    fontsize=12)
    ax.set_xlabel('Subjects', fontsize=14)
    ax.set_ylabel('Marks', fontsize=14)
    sns.despine(fig)
    return fig


# Function to analyze subject performance
def analyze_subject_performance(df, subjects):
    weak_subjects = []
    strong_subjects = []
    avg_marks = df[subjects].mean()
    
    for subject in subjects:
        if avg_marks[subject] < 60:
            weak_subjects.append(subject)
        else:
            strong_subjects.append(subject)
    
    return weak_subjects, strong_subjects, avg_marks

# Function to get subject-specific improvement suggestions from Gemini
@st.cache_data
def get_subject_suggestions(subject):
    prompt = f"""
    The class is struggling in {subject}. Provide brief strategies to help students improve in this subject (50 words max):
    - Additional classes or tutoring
    - Recommended study resources or activities
    - Tips to improve understanding and retention of material
    - Methods to boost motivation and engagement in the subject

    Let's take an example for geography, change this as per the subject:
    Actively participate in class discussions. Share your thoughts and questions!
    Explore online resources like YouTube educational channels. They can offer additional explanations and diverse perspectives.
    Utilize AI tools for extra practice. These tools can provide personalized exercises to solidify your understanding.
    Form study groups with classmates who share similar interests. Discuss notes, solve problems together, and test each other's knowledge.
    Engage in hands-on activities like map quizzes or geography games. Learning can be fun and interactive!
    Seek additional help from teachers or tutors if you face specific challenges. They're here to support you!
    Maintain consistent attendance and focus during class. This will maximize your learning potential.  

    Make sure to keep this in bullet points not exceeding 3 and give the best response based on the example that I provided and the rules
    """

    # Use Gemini API (configured earlier with GEMINI_API_KEY from .env)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)

    return response.text.strip() if response and hasattr(response, "text") else "No suggestions generated."


# Function to get attendance insights
def attendance_insights(df):
    avg_attendance = df['Attendance'].mean()
    min_attendance = df['Attendance'].min()
    max_attendance = df['Attendance'].max()
    
    avg_marks = df[[col for col in df.columns if col not in ['Roll No', 'Name', 'Attendance']]].mean(axis=1)
    correlation = df['Attendance'].corr(avg_marks)
    
    if correlation > 0.5:
        attendance_impact = "Low attendance is significantly impacting performance. Ensure regular attendance."
    elif correlation > 0:
        attendance_impact = "Attendance is moderately impacting performance. Try to attend more regularly."
    else:
        attendance_impact = "Attendance is not a major issue for performance. Focus on study habits and concentration."
    
    lowest_attendance_student = df[df['Attendance'] == min_attendance]['Name'].values[0]
    highest_attendance_student = df[df['Attendance'] == max_attendance]['Name'].values[0]
    
    insights = f"""
    - Average Attendance: {avg_attendance:.2f}%
    - Lowest Attendance: {min_attendance}% (Student: {lowest_attendance_student})
    - Highest Attendance: {max_attendance}% (Student: {highest_attendance_student})
    - Insights: {attendance_impact}
    """
    return insights


# Function to save insights to a docx file
def save_insights_to_docx(title, insights, charts):
    doc = Document()
    doc.add_heading(title, level=1)
    for insight in insights.split('\n'):
        if insight.strip():
            p = doc.add_paragraph(insight.strip(), style='BodyText')
            for run in p.runs:
                run.font.size = Pt(12)
    for chart in charts:
        image_stream = BytesIO()
        chart.savefig(image_stream, format='png')
        image_stream.seek(0)
        doc.add_picture(image_stream, width=docx.shared.Inches(6))
    return doc


def analysis():
    uploaded_file = st.file_uploader("Upload CSV file with student data", type="csv")
    analysis_type = st.sidebar.radio(
        "Choose Analysis Type:",
        ["Class Wide Performance Analysis", "Student Wise Performance Analysis", "Attendance Analysis", "Ask Questions To The Data"],
        horizontal=False
    )

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        required_columns = ['Roll No', 'Name', 'Attendance']

        if not all(col in df.columns for col in required_columns):
            st.error("CSV file must contain 'Roll No', 'Name', and 'Attendance' columns.")
            return

        subjects = [col for col in df.columns if col not in required_columns]

        # -------------------- STUDENT-WISE PERFORMANCE --------------------
        if analysis_type == "Student Wise Performance Analysis":
            st.markdown("<h1 style='font-size:30px;font-family:Garamond,serif;'>Student-wise Analysis</h1>", unsafe_allow_html=True)
            student_names = df['Name'].unique()
            selected_student = st.selectbox("Select a student to analyze:", student_names)

            student_data = df[df['Name'] == selected_student].iloc[0]
            marks = {subject: student_data[subject] for subject in subjects}
            attendance = student_data['Attendance']
            overall_score = calculate_performance(list(marks.values()))

            st.markdown(f"<h1 style='font-size:30px;font-family:Garamond,serif;'>{selected_student}'s Performance</h1>", unsafe_allow_html=True)
            st.write(f"Average Score: {overall_score:.2f}/100")
            st.write(f"Attendance: {attendance}%")

            fig = plot_performance(subjects, list(marks.values()), f"{selected_student}'s Subject-wise Marks")
            st.pyplot(fig)

            categories = {
                'Excellent': 90,
                'Good': 80,
                'Needs Improvement': 60,
                'Concerning': 40,
                'Failed': 0
            }

            st.markdown("<h1 style='font-size:30px;font-family:Garamond,serif;'>Subject-wise Status</h1>", unsafe_allow_html=True)
            for subject, mark in marks.items():
                for cat, threshold in categories.items():
                    if mark >= threshold:
                        st.write(f"{subject}: {cat} ({mark}/100)")
                        break

            if attendance < 50:
                st.error("🚨 CRITICAL WARNING: Attendance is dangerously low. Immediate action is required.")
            elif attendance < 75:
                st.warning("⚠ Attendance is below 75%. This can significantly impact performance.")

            st.markdown("<h1 style='font-size:30px;font-family:Garamond,serif;'>Personalized Suggestions</h1>", unsafe_allow_html=True)
            suggestions = get_suggestions(selected_student, marks, attendance)
            st.write(suggestions)

            charts = [fig]
            doc = save_insights_to_docx(f"{selected_student}'s Performance Insights", suggestions, charts)
            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)
            st.download_button(
                label="Download Student Insights",
                data=buffer,
                file_name=f"{selected_student}_insights.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # -------------------- CLASS-WIDE PERFORMANCE --------------------
        elif analysis_type == "Class Wide Performance Analysis":
            st.markdown("<h1 style='font-size:30px;font-family:Garamond,serif;'>Class-wide Analysis</h1>", unsafe_allow_html=True)

            class_avg = df[subjects].mean().mean()
            weak_subjects, strong_subjects, avg_marks = analyze_subject_performance(df, subjects)

            st.markdown("<h1 style='font-size:30px;font-family:Garamond,serif;'>Subjects Analysis</h1>", unsafe_allow_html=True)
            st.write("Subjects where students are performing well:")
            for subject in strong_subjects:
                st.write(f"- {subject}: {avg_marks[subject]:.2f}/100")

            st.write("Subjects where students are struggling:")
            for subject in weak_subjects:
                st.write(f"- {subject}: {avg_marks[subject]:.2f}/100")

            avg_marks_series = df[subjects].mean()
            highest_marks = df[subjects].max()
            lowest_marks = df[subjects].min()

            display_cards("Class Subject Performance", avg_marks_series.mean(), highest_marks.max(), lowest_marks.min())

            selected_subject = st.selectbox("Select a weak subject to get improvement suggestions:", weak_subjects)
            if selected_subject:
                st.write(f"*Suggestions to Improve Performance in {selected_subject}:*")
                subject_suggestions = get_subject_suggestions(selected_subject)
                st.write(subject_suggestions)

            st.markdown("<h1 style='font-size:30px;font-family:Garamond,serif;'>Overall Class Improvement Plan</h1>", unsafe_allow_html=True)
            class_suggestions = get_class_suggestions(avg_marks_series.to_dict())
            st.write(class_suggestions)

            class_doc = Document()
            class_doc.add_heading("Class-wide Performance Insights", level=1)
            class_doc.add_heading("Subjects Analysis", level=2)

            class_doc.add_heading("Subjects where students are performing well:", level=3)
            for subject in strong_subjects:
                p = class_doc.add_paragraph(f"- {subject}: {avg_marks[subject]:.2f}/100", style='BodyText')
                for run in p.runs:
                    run.font.size = Pt(12)

            class_doc.add_heading("Subjects where students are struggling:", level=3)
            for subject in weak_subjects:
                p = class_doc.add_paragraph(f"- {subject}: {avg_marks[subject]:.2f}/100", style='BodyText')
                for run in p.runs:
                    run.font.size = Pt(12)

            class_doc.add_heading("Overall Class Improvement Plan", level=2)
            p = class_doc.add_paragraph(class_suggestions, style='BodyText')
            for run in p.runs:
                run.font.size = Pt(12)

            buffer = BytesIO()
            class_doc.save(buffer)
            buffer.seek(0)
            st.download_button(
                label="Download Class Insights",
                data=buffer,
                file_name="class_insights.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # -------------------- ASK QUESTIONS TO THE DATA --------------------
        elif analysis_type == "Ask Questions To The Data":
            question = st.text_area("Ask a question about the dataset:")

            if st.button("Get Answer"):
                context = df.to_string(index=False)
                answer = query_gemini(question, context)
                st.success(answer)

    else:
        st.info("Please upload a CSV file with the following columns: Roll No, Name, Attendance, and at least one subject column.")


if __name__ == "__main__":
    analysis()