import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from app.schemas import StudyAnswer
from app.mcq_schema import MCQResponse

load_dotenv()

model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def generate_study_answer(prompt: str) -> StudyAnswer:
    structured_model = model.with_structured_output(StudyAnswer)
    response = structured_model.invoke(prompt)
    return response


def generate_mcqs(prompt: str) -> MCQResponse:
    structured_model = model.with_structured_output(MCQResponse)
    response = structured_model.invoke(prompt)
    return response


def generate_text(prompt: str) -> str:
    response = model.invoke(prompt)
    return response.content