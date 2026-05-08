/* eslint-disable */
import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [workouts, setWorkouts] = useState([]);
  const [formData, setFormData] = useState({
    exercise_name: '',
    sets: '',
    reps: '',
    weight: ''
  });

  // Dynamically uses your EC2 IP from GitHub Actions, or localhost if you are on your laptop
  const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/workouts/';

  const fetchWorkouts = async () => {
    try {
      const response = await axios.get(API_URL);
      setWorkouts(response.data);
    } catch (error) {
      console.error("Error fetching workouts:", error);
    }
  };

  useEffect(() => {
    fetchWorkouts();
  }, []);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post(API_URL, formData);
      setFormData({ exercise_name: '', sets: '', reps: '', weight: '' });
      fetchWorkouts();
    } catch (error) {
      console.error("Error saving workout:", error);
    }
  };

  return (
    <div className="container">
      <h1>🏋️ Minimalist Workout Tracker</h1>

      <div className="card">
        <h2>Log a New Workout</h2>
        <form onSubmit={handleSubmit} className="workout-form">
          <input 
            type="text" name="exercise_name" placeholder="Exercise (e.g., Bench Press)" 
            value={formData.exercise_name} onChange={handleInputChange} required 
          />
          <input 
            type="number" name="sets" placeholder="Sets" 
            value={formData.sets} onChange={handleInputChange} required 
          />
          <input 
            type="number" name="reps" placeholder="Reps" 
            value={formData.reps} onChange={handleInputChange} required 
          />
          <input 
            type="number" step="0.1" name="weight" placeholder="Weight (kg/lbs)" 
            value={formData.weight} onChange={handleInputChange} required 
          />
          <button type="submit">Log Workout</button>
        </form>
      </div>

      <div className="card">
        <h2>Workout History</h2>
        {workouts.length === 0 ? (
          <p>No workouts logged yet. Get lifting!</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Exercise</th>
                <th>Sets</th>
                <th>Reps</th>
                <th>Weight</th>
              </tr>
            </thead>
            <tbody>
              {workouts.map((workout) => (
                <tr key={workout.id}>
                  <td>{new Date(workout.date).toLocaleDateString()}</td>
                  <td>{workout.exercise_name}</td>
                  <td>{workout.sets}</td>
                  <td>{workout.reps}</td>
                  <td>{workout.weight}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default App;