import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [workouts, setWorkouts] = useState([]);
  const [title, setTitle] = useState("");
  const [duration, setDuration] = useState("");
  const navigate = useNavigate();

  // SAFE token inside functions
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    fetchWorkouts(token);
  }, []);

  function fetchWorkouts(token) {
    fetch("http://127.0.0.1:5555/api/workouts", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("GET:", data);

        if (Array.isArray(data)) {
          setWorkouts(data);
        } else {
          setWorkouts([]);
        }
      })
      .catch((err) => {
        console.log("GET ERROR:", err);
        setWorkouts([]);
      });
  }

  function addWorkout() {
    const token = localStorage.getItem("token");

    if (!token) return;

    fetch("http://127.0.0.1:5555/api/workouts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ title, duration }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("ADD:", data);

        if (data.id) {
          setWorkouts((prev) => [...prev, data]);
          setTitle("");
          setDuration("");
        }
      });
  }

  function deleteWorkout(id) {
    const token = localStorage.getItem("token");

    fetch(`http://127.0.0.1:5555/api/workouts/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }).then(() => {
      setWorkouts((prev) => prev.filter((w) => w.id !== id));
    });
  }

  return (
    <div style={{ padding: "20px", maxWidth: "500px", margin: "0 auto" }}>
      <h2>Dashboard</h2>

      <input
        placeholder="title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <input
        placeholder="duration"
        value={duration}
        onChange={(e) => setDuration(e.target.value)}
      />

      <button onClick={addWorkout}>Add</button>

      <hr />

      {workouts.length === 0 ? (
        <p>No workouts</p>
      ) : (
        workouts.map((w) => (
          <div key={w.id}>
            {w.title} - {w.duration}
            <button onClick={() => deleteWorkout(w.id)}>X</button>
          </div>
        ))
      )}
    </div>
  );
}
