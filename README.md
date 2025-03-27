# EduEase

EduEase is a versatile platform designed to alleviate the workload of teachers. It offers a unified interface where educators can effortlessly generate quizzes and lesson plans, track student performance both on a class-wide and individual level, and summarize lessons. Additionally, EduEase provides a space for mental well-being support, ensuring teachers receive the care they need while focusing on their students. The platform streamlines various tasks, empowering teachers to manage their responsibilities more efficiently and focus on fostering a better learning environment.

## Contributors
   1.[Vennela Varshini Anasoori](https://www.linkedin.com/in/vennela-varshini-anasoori/)
   2.[Hansika Reddy](https://www.linkedin.com/in/hansika-reddy-a32361325/)
   3.[Sindhuja Pagadala](https://www.linkedin.com/in/sindhuja-pagadala-a5a290325/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)
   4.[Khushi Arya](https://www.linkedin.com/in/khushi-arya-aa1515327/?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)

## Inspiration
   In recent times, educators in schools, coaching centers, and colleges often struggle with overwhelming workloads, especially when tasked with providing individualized feedback to students in large classrooms. The high teacher-to-student ratios exacerbate this issue, leaving educators with limited time to focus on their core responsibilities of teaching and mentoring. As a result, teachers are increasingly prone to stress and burnout, often lacking adequate support, which hinders their ability to efficiently manage their responsibilities.

## Features

- **Perform Analysis**: Allows teachers to analyse the progress and regularity of students:
  - Class wide and student wise analysis of grades in each subject.
  - Attendance analysis.
  - Custom queries allowed to the input data for more personalised analysis.

- **Generate Quizzes and Lesson plans**: Allow teachers to:
  - Generate quizzes and MCQ's based on topic and can customise the difficulty level and no. of questions.
  - Generate lesson plan based on the topic and can customise no. of sessions and no. of hours per session.

- **Summarise Lessons**: Reduces the burden over the teachers by:
  - Lesson summary (when input text data on required topic is provided).

- **Virtual AI counsellor**: A compassionate, human-centered chatbot designed to provide mental support and offer personalized suggestions to overburdened teachers.



## Getting Started

### Prerequisites

Ensure you have the following installed before running the project:

- **Python (>=3.8)**
- **pip (Python package manager)**
- **Git** (optional but recommended)

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vennelavarshini18/EduEase.git
   ```
2. **Navigate to the project directory**:
   ```bash
   cd EduEase
   ```
3. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   ```
4. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```
5. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Setting Up Environment Variables

1. **Create a `.env` file** in the project's root directory:
   ```bash
   touch .env
   ```
2. **Open the `.env` file** and add the following (replace with actual values):
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_genai_api_key_here
   ```
3. **Ensure that `.env` is listed in `.gitignore`** to prevent exposing sensitive information.

### Running the Application

After installation, follow these steps to run the project:

1. **Start the application**:
   ```bash
   streamlit run main.py
   ```
2. Open your browser and go to:
   ```
   https://127.0.0.1:5000/
   ```
   (or the address displayed in your terminal)

## Project Structure

```
EduEase/
│-- main.py               # Entry point of the application
│-- LessonPlan.py         # Manages lesson planning functionalities
│-- MCQ.py                # Handles multiple-choice questions
│-- animations.py         # Contains animation-related functions
│-- customquery.py        # Manages custom queries from users
│-- dataset_for_hackprix.csv  # Dataset used for the project
│-- lessonsummarize.py    # Summarizes lesson content
│-- teacheranalysis.py    # Analyzes teacher performance
│-- wellness.py           # Manages student wellness features
│-- .env                  # Stores environment variables (DO NOT SHARE)
│-- requirements.txt      # Lists the Python dependencies
│-- static/               # Contains static assets (CSS, JavaScript, images)
│-- templates/            # HTML templates for the web interface
```

## Contact

For any questions or feedback, please contact [vennelavarshini18](https://github.com/vennelavarshini18).