import React from "react";
import "./App.css";
import Lottie from "lottie-react";
import studentAnimation from "./STUDENT.json"; // Lottie animation JSON
import { FaChalkboardTeacher, 
  FaClipboardList, 
  FaUserGraduate, 
  FaUsers, 
  FaCalendarCheck, 
  FaRobot, 
  FaQuestionCircle 
} from "react-icons/fa";


export default function App() {
  return (
    <div className="hero-container">
      {/* Navbar */}
      <nav className="navbar">
        <div className="logo">EduEase</div>
        <ul className="nav-links">
          <li className="active">Home</li>
          <li>Features</li>
          <li>AboutUs</li>
          <li>Contact</li>
        </ul>
        <button
  className="login-btn"
  onClick={() => {
    window.location.href = "http://localhost:8501";
  }}
>
  Login
</button>
      </nav>

      {/* Hero Section */}
      <div className="hero-content">
        {/* Left Text Section */}
        <div className="hero-text">
          <h1>
            Simplifying Education for <br />
            <span>All</span>
          </h1>
          <h3>Your Smart Assignment & Quiz Platform</h3>
          <p>
            EduEase makes learning interactive and grading effortless. 
            Teachers can create quizzes, students can submit instantly, 
            and AI handles the evaluation with personalized feedback.
          </p>
          <button className="get-started">Get Started</button>
        </div>

        {/* Right Animation Section */}
        <div className="hero-image">
          <Lottie 
            animationData={studentAnimation} 
            loop={true} 
            style={{ width: 450, height: 550 }} 
          />
        </div>
      </div>

      {/* Features Section */}
      <section className="features-section">
      <div className="features-grid">
  <div className="feature-card">
    <div className="feature-icon"><FaChalkboardTeacher /></div>
    <h3>Lesson Plan Generation</h3>
    <p>Create structured, AI-generated lesson plans tailored to your teaching goals.</p>
  </div>

  <div className="feature-card">
    <div className="feature-icon"><FaClipboardList /></div>
    <h3>Lesson Summaries</h3>
    <p>Automatically generate concise summaries for quick student revision.</p>
  </div>

  <div className="feature-card">
    <div className="feature-icon"><FaUserGraduate /></div>
    <h3>Personalised Analysis</h3>
    <p>Track each student’s performance with in-depth, AI-powered analytics.</p>
  </div>

  <div className="feature-card">
    <div className="feature-icon"><FaUsers /></div>
    <h3>Collaborative Learning</h3>
    <p>Encourage peer-to-peer engagement with group activities and shared resources.</p>
  </div>

  <div className="feature-card">
    <div className="feature-icon"><FaCalendarCheck /></div>
    <h3>Smart Scheduling</h3>
    <p>Organise classes, assignments, and deadlines with AI-powered reminders.</p>
  </div>

  <div className="feature-card">
    <div className="feature-icon"><FaRobot /></div>
    <h3>AI Tutoring</h3>
    <p>Offer students instant, AI-driven assistance for homework and queries.</p>
  </div>
</div>
</section>
    </div>
  );
}
