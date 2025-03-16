# EduEase

EduEase is a comprehensive platform designed to centralize academic resources for college students. It provides a unified space where students can access class schedules, club events, and other academic-related materials.

## Features

- **Class Management**: Maintain a daily class schedule calendar. Class representatives can:
  - Post updates.
  - Revise class statuses (e.g., canceled, postponed).
  - Edit schedules.
  - Post notices.
  - Students can opt-in to receive class reminders and notifications.

- **Club Management**: Allow clubs (including NSS and other semi-club bodies) to:
  - Post event notifications.
  - Maintain an event calendar.
  - Students can subscribe to individual events or all activities of a club.

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

### Running the Application

After installation, follow these steps to run the project:

1. **Start the application**:
   ```bash
   python main.py
   ```
2. Open your browser and go to:
   ```
   http://127.0.0.1:5000/
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
│-- requirements.txt      # Lists the Python dependencies
│-- static/               # Contains static assets (CSS, JavaScript, images)
│-- templates/            # HTML templates for the web interface
```

## Contributing

We welcome contributions to enhance EduEase. To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request detailing your changes.

## Contact

For any questions or feedback, please contact [vennelavarshini18](https://github.com/vennelavarshini18).