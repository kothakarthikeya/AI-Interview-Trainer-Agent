from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# IBM Watsonx model
model = ModelInference(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials={
        "apikey": os.getenv("IBM_API_KEY"),
        "url": os.getenv("IBM_URL")
    },
    project_id=os.getenv("PROJECT_ID")
)

# Store latest question temporarily
latest_question = ""

# Home Page
@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>

    <head>

        <title>AI Interview Trainer</title>

        <style>

            body{
                font-family: Arial;
                background:#f4f4f4;
                padding:40px;
            }

            .container{
                background:white;
                width:650px;
                margin:auto;
                padding:30px;
                border-radius:12px;
                box-shadow:0px 0px 10px rgba(0,0,0,0.1);
            }

            h1{
                text-align:center;
            }

            select,button{
                width:100%;
                padding:12px;
                margin-top:15px;
                border-radius:6px;
                font-size:16px;
            }

            button{
                background:#0070f3;
                color:white;
                border:none;
                cursor:pointer;
            }

            button:hover{
                background:#0057c2;
            }

        </style>

    </head>

    <body>

        <div class="container">

            <h1>AI Interview Trainer</h1>

            <form action="/generate" method="post">

                <label><b>Select Skill</b></label>

                <select name="skill">

                    <option>Python</option>
                    <option>Java</option>
                    <option>React</option>
                    <option>JavaScript</option>
                    <option>Machine Learning</option>
                    <option>DBMS</option>

                </select>

                <label><b>Select Difficulty</b></label>

                <select name="level">

                    <option>Easy</option>
                    <option>Medium</option>
                    <option>Hard</option>

                </select>

                <button type="submit">
                    Start Interview
                </button>

            </form>

        </div>

    </body>

    </html>
    """


# Generate Question
@app.post("/generate", response_class=HTMLResponse)
def generate(
    skill: str = Form(...),
    level: str = Form(...)
):

    global latest_question

    prompt = f"""
    Generate ONE high-quality interview question.

    Skill: {skill}
    Difficulty: {level}

    Requirements:
    - Ask realistic technical interview question
    - Keep it concise
    - Return only question
    """

    response = model.generate_text(
        prompt=prompt,
        params={
            "max_new_tokens": 120,
            "temperature": 0.7
        }
    )

    latest_question = response.strip()

    return f"""
    <html>

    <head>

        <title>Interview Question</title>

        <style>

            body{{
                font-family:Arial;
                background:#f4f4f4;
                padding:40px;
            }}

            .container{{
                background:white;
                width:800px;
                margin:auto;
                padding:30px;
                border-radius:12px;
                box-shadow:0px 0px 10px rgba(0,0,0,0.1);
            }}

            textarea{{
                width:100%;
                height:180px;
                padding:10px;
                margin-top:20px;
                font-size:16px;
            }}

            button{{
                margin-top:20px;
                padding:12px 20px;
                background:#0070f3;
                color:white;
                border:none;
                border-radius:6px;
                cursor:pointer;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>Interview Question</h1>

            <h2>{latest_question}</h2>

            <form action="/evaluate" method="post">

                <textarea 
                    name="answer"
                    placeholder="Type your answer here..."
                ></textarea>

                <button type="submit">
                    Submit Answer
                </button>

            </form>

        </div>

    </body>

    </html>
    """


# Evaluate Answer
@app.post("/evaluate", response_class=HTMLResponse)
def evaluate(answer: str = Form(...)):

    global latest_question

    evaluation_prompt = f"""
    You are an expert technical interviewer.

    Interview Question:
    {latest_question}

    Candidate Answer:
    {answer}

    Evaluate the answer and provide:

    1. Score out of 10
    2. Strengths
    3. Improvements
    4. Correct Answer Summary

    Keep evaluation professional and concise.
    """

    evaluation = model.generate_text(
        prompt=evaluation_prompt,
        params={
            "max_new_tokens": 400,
            "temperature": 0.5
        }
    )

    return f"""
    <html>

    <head>

        <title>Evaluation Result</title>

        <style>

            body{{
                font-family:Arial;
                background:#f4f4f4;
                padding:40px;
            }}

            .container{{
                background:white;
                width:850px;
                margin:auto;
                padding:30px;
                border-radius:12px;
                box-shadow:0px 0px 10px rgba(0,0,0,0.1);
            }}

            pre{{
                white-space:pre-wrap;
                line-height:1.8;
                font-size:16px;
            }}

            button{{
                margin-top:20px;
                padding:12px 20px;
                background:#0070f3;
                color:white;
                border:none;
                border-radius:6px;
                cursor:pointer;
            }}

        </style>

    </head>

    <body>

        <div class="container">

            <h1>AI Evaluation Result</h1>

            <pre>{evaluation}</pre>

            <a href="/">
                <button>
                    Start New Interview
                </button>
            </a>

        </div>

    </body>

    </html>
    """