import "./css/About.css";
import { useNavigate } from "react-router-dom";

function About() {
  const navigate = useNavigate();

  return (
    <>
      <nav>
        <div className="left">Task management system</div>
        <div className="menu-toggle">
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
        </div>

        <div className="right">
          <ul id="nav-list">
            <li><a href="/Dashboard">Dashboard</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Tasks</a></li>
            <li><a href="#">Profile</a></li>
          </ul>
        </div>
      </nav>
      <main className="about-page">
        <section className="about-container">
          <h1>About the Project</h1>

          <p className="intro">
            The <strong>Task Management System</strong> is a modern web application
            designed to simplify task assignment, tracking, and management for
            teams and individuals. It provides a centralized platform to organize
            work efficiently and improve productivity.
          </p>

          <section className="about-section">
            <h2>Why This Project?</h2>
            <p>
              Managing tasks using scattered tools or manual methods often leads
              to missed deadlines and poor visibility. This system solves that
              problem by offering a structured, role-based workflow where tasks
              are clearly assigned, tracked, and reviewed.
            </p>
          </section>

          <section className="about-section">
            <h2>Key Features</h2>
            <ul>
              <li>Role-based authentication (Admin & User)</li>
              <li>Task assignment with deadlines</li>
              <li>Task review and status tracking</li>
              <li>Responsive dashboard for all devices</li>
              <li>Secure and user-friendly interface</li>
            </ul>
          </section>

          <section className="about-section">
            <h2>Who Can Use It?</h2>
            <p>
              This application is ideal for students, small teams, project
              managers, and organizations that need a simple yet effective way to
              manage tasks and workflows.
            </p>
          </section>

          <section className="about-section">
            <h2>Technology Stack</h2>
            <ul>
              <li><strong>Frontend:</strong> React.js, HTML5, CSS3</li>
              <li><strong>Backend:</strong> REST APIs</li>
              <li><strong>Database:</strong> MySQL</li>
              <li><strong>Authentication:</strong> JWT-based authentication</li>
            </ul>
          </section>

          <section className="about-section">
            <h2>Future Enhancements</h2>
            <ul>
              <li>Real-time notifications</li>
              <li>Task analytics and reports</li>
              <li>File attachments</li>
              <li>Team collaboration features</li>
            </ul>
          </section>
        </section>
      </main>
    </>
  );
}

export default About;
