import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  function register(e) {
    e.preventDefault();

    fetch("http://127.0.0.1:5555/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    }).then(() => navigate("/"));
  }

  return (
    <div>
      <h2>Register</h2>

      <form onSubmit={register}>
        <input
          onChange={(e) => setUsername(e.target.value)}
          placeholder="username"
        />
        <input
          type="password"
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
        />
        <button>Register</button>
      </form>

      <Link to="/">Login</Link>
    </div>
  );
}
