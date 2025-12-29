import { useNavigate } from "react-router-dom";
import "./css/Login.css";
import { useState } from "react";
import {  toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import axios from "axios";
import { CONFIG } from "../../config/CONFIG";
import { setToken } from "../../util/manageToken";



function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const login = async () => {
    if (email !== "" && password !== "") {
      try {
        const res = await axios.post(CONFIG.BASE_URL + "/auth/login", {
          "name": email,
          "password": password
        })
        let newToken = res?.data?.access_token;
        localStorage.setItem("token", newToken);
        setToken(newToken);
        toast.success("Login successful!");
        setTimeout(() => {
          navigate("/Dashboard");
        }, 1000);
      } catch (err) {
        toast.error("Login Failed!");
        console.log("err- ", err)
      }

    } else {
      toast.error("Invalid email or password");
    }
  };

  return (
    <>
      {/* NAVBAR */}
      <nav>
        <div className="left">Task management system</div>
        <div className="menu-toggle">
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
        </div>

        <div className="right">
          <ul id="nav-list">
            {/* <li><a href="#">Dashboard</a></li> */}
            <li><a href="/about">About</a></li>
            {/* <li><a href="#">Tasks</a></li>
            <li><a href="#">Profile</a></li> */}
          </ul>
        </div>
      </nav>

      {/* LOGIN */}
      <div className="login-wrapper">
        <div className="login-container">
          <h2>Welcome Back</h2>
          <p>Login to your Task Management System</p>

          <div className="field">
            <label>Name</label>
            <input
              type="text"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="field">
            <label>Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button className="login-btn" onClick={login}>
            Login
          </button>

          <div className="footer-text">
            © <span>Aryan's Task Management</span>
          </div>
        </div>
      </div>

      
    </>
  );
}

export default Login;
