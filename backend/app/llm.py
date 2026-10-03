from langchain_ollama import ChatOllama

from app.schemas import StudyAnswer
from app.mcq_schema import MCQResponse


model = ChatOllama(
    model="llama3.1:8b",
    temperature=0.7
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