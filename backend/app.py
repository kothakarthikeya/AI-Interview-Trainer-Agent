from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IBM Model
model = ModelInference(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials={
        "apikey": os.getenv("IBM_API_KEY"),
        "url": os.getenv("IBM_URL")
    },
    project_id=os.getenv("PROJECT_ID")
)

# Store latest question
latest_question = ""


# Home Route
@app.get("/")
def home():
    return {
        "message": "AI Interview Trainer Backend Running"
    }


# Generate Question
@app.post("/generate")
def generate(skill: str = Form(...), level: str = Form(...)):

    global latest_question

    prompt = f"""
    Generate ONE professional technical interview question.

    Skill: {skill}
    Difficulty: {level}

    Requirements:
    - Ask only one question
    - Make it realistic
    - Technical interview style
    - Return only the question
    """

    response = model.generate_text(
        prompt=prompt,
        params={
            "max_new_tokens": 120,
            "temperature": 0.7
        }
    )

    latest_question = response.strip()

    return {
        "question": latest_question
    }


# Evaluate Answer
@app.post("/evaluate")
def evaluate(answer: str = Form(...)):

    global latest_question

    prompt = f"""
    You are an expert technical interviewer.

    Interview Question:
    {latest_question}

    Candidate Answer:
    {answer}

    Evaluate the answer and provide:

    1. Score out of 10
    2. Strengths
    3. Weaknesses
    4. Correct Answer Summary

    Keep evaluation concise and professional.
    """

    evaluation = model.generate_text(
        prompt=prompt,
        params={
            "max_new_tokens": 400,
            "temperature": 0.5
        }
    )

    return {
        "evaluation": evaluation
    }