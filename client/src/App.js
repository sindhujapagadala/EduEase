import React from "react";
import "./App.css";
import Lottie from "lottie-react";
import studentAnimation from "./STUDENT.json";
import {
  FaChalkboardTeacher,
  FaClipboardList,
  FaUserGraduate,
  FaUsers,
  FaCalendarCheck,
  FaRobot,
  FaFacebook,
  FaTwitter,
  FaInstagram,
  FaLinkedin,
  FaMapMarkerAlt,
  FaPhone,
  FaEnvelope
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
        <h2 className="features-title">Our Features</h2>
        <div className="features-grid">
          {features.map((feature, index) => (
            <div className="feature-card" key={index}>
              <div className="feature-icon">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Why Choose Us Section */}
      <section className="why-choose-us">
        <div className="why-container">
          <div className="why-image">
            <img
              src="https://images.pexels.com/photos/4491461/pexels-photo-4491461.jpeg"
              alt="Teacher explaining"
            />
          </div>
          <div className="why-text">
            <h2>Why Choose Us</h2>
            <p>
              Our platform is designed by educators for educators, combining
              cutting-edge technology with pedagogical expertise to transform
              the learning experience.
            </p>
            <ul>
              <li>✔ AI-powered personalized learning paths</li>
              <li>✔ Real-time performance analytics</li>
              <li>✔ Intuitive interface for all age groups</li>
              <li>✔ Secure and privacy-focused</li>
              <li>✔ Continuous platform improvements</li>
              <li>✔ 24/7 dedicated support</li>
            </ul>
            <button className="learn-more-btn">Learn More</button>
          </div>
        </div>
      </section>

      {/* Footer Section */}
      <footer className="footer">
        <div className="footer-container">
          <div className="footer-column">
            <h3>EduEase</h3>
            <p>Transforming education through innovative technology solutions that make learning accessible, engaging, and effective for everyone.</p>
            <div className="social-icons">
              <a href="#"><FaFacebook /></a>
              <a href="#"><FaTwitter /></a>
              <a href="#"><FaInstagram /></a>
              <a href="#"><FaLinkedin /></a>
            </div>
          </div>

          <div className="footer-column">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="#">Home</a></li>
              <li><a href="#">Features</a></li>
              <li><a href="#">Pricing</a></li>
              <li><a href="#">About Us</a></li>
              <li><a href="#">Contact</a></li>
            </ul>
          </div>

          <div className="footer-column">
            <h3>Resources</h3>
            <ul>
              <li><a href="#">Blog</a></li>
              <li><a href="#">Help Center</a></li>
              <li><a href="#">Tutorials</a></li>
              <li><a href="#">Webinars</a></li>
              <li><a href="#">API Docs</a></li>
            </ul>
          </div>

          <div className="footer-column">
            <h3>Contact Us</h3>
            <ul className="contact-info">
              <li><FaMapMarkerAlt /> 123 Education St, Tech City</li>
              <li><FaPhone /> +1 (555) 123-4567</li>
              <li><FaEnvelope /> info@eduease.com</li>
            </ul>
          </div>
        </div>

        <div className="footer-bottom">
          <p>&copy; {new Date().getFullYear()} EduEase. All rights reserved.</p>
          <div className="legal-links">
            <a href="#">Privacy Policy</a>
            <a href="#">Terms of Service</a>
            <a href="#">Cookie Policy</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

const features = [
  {
    icon: <FaChalkboardTeacher />,
    title: "Lesson Plan Generation",
    description: "Create structured, AI-generated lesson plans tailored to your teaching goals."
  },
  {
    icon: <FaClipboardList />,
    title: "Lesson Summaries",
    description: "Automatically generate concise summaries for quick student revision."
  },
  {
    icon: <FaUserGraduate />,
    title: "Personalised Analysis",
    description: "Track each student's performance with in-depth, AI-powered analytics."
  },
  {
    icon: <FaUsers />,
    title: "Collaborative Learning",
    description: "Encourage peer-to-peer engagement with group activities and shared resources."
  },
  {
    icon: <FaCalendarCheck />,
    title: "Smart Scheduling",
    description: "Organize classes, assignments, and deadlines with AI-powered reminders."
  },
  {
    icon: <FaRobot />,
    title: "AI Tutoring",
    description: "Offer students instant, AI-driven assistance for homework and queries."
  }
];