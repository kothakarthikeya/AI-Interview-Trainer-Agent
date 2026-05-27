import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [skill, setSkill] = useState("Python");
  const [level, setLevel] = useState("Easy");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState("");
  const [loading, setLoading] = useState(false);

  // Generate Question
  const generateQuestion = async () => {

    setLoading(true);
    setEvaluation("");

    try {

      const formData = new FormData();

      formData.append("skill", skill);
      formData.append("level", level);

      const response = await axios.post(
        "http://127.0.0.1:8000/generate",
        formData
      );

      setQuestion(response.data.question);

    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  };

  // Evaluate Answer
  const evaluateAnswer = async () => {

    setLoading(true);

    try {

      const formData = new FormData();

      formData.append("answer", answer);

      const response = await axios.post(
        "http://127.0.0.1:8000/evaluate",
        formData
      );

      setEvaluation(response.data.evaluation);

    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  };

  return (

    <div className="app">

      <div className="navbar">
        <h1>AI Interview Trainer</h1>
      </div>

      <div className="container">

        <div className="card">

          <h2>Generate Interview Question</h2>

          <label>Select Skill</label>

          <select
            value={skill}
            onChange={(e) => setSkill(e.target.value)}
          >
            <option>Python</option>
            <option>Java</option>
            <option>React</option>
            <option>JavaScript</option>
            <option>Machine Learning</option>
            <option>DBMS</option>
            <option>Operating Systems</option>
            <option>Computer Networks</option>
          </select>

          <label>Select Difficulty</label>

          <select
            value={level}
            onChange={(e) => setLevel(e.target.value)}
          >
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>

          <button onClick={generateQuestion}>
            {loading ? "Generating..." : "Generate Question"}
          </button>

        </div>

        {question && (

          <div className="card">

            <h2>Interview Question</h2>

            <p className="question">{question}</p>

            <textarea
              placeholder="Write your answer here..."
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
            />

            <button onClick={evaluateAnswer}>
              Evaluate Answer
            </button>

          </div>

        )}

        {evaluation && (

          <div className="card">

            <h2>AI Evaluation</h2>

            <pre>{evaluation}</pre>

          </div>

        )}

      </div>

    </div>

  );
}

export default App;