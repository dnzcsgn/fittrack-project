import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function handleLogin(e) {
    e.preventDefault();

    fetch("http://127.0.0.1:5555/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("LOGIN RESPONSE:", data);

        if (data.token) {
          localStorage.setItem("token", data.token);
          console.log("TOKEN SAVED:", data.token);
          navigate("/dashboard");
        } else {
          alert("Login failed: no token received");
        }
      })
      .catch((err) => {
        console.log("LOGIN ERROR:", err);
        alert("Server error");
      });
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Login</h2>

      <form onSubmit={handleLogin}>
        <input
          placeholder="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <br />
        <br />

        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <br />
        <br />

        <button type="submit">Login</button>
      </form>

      <br />

      <Link to="/register">Go to Register</Link>
    </div>
  );
}
