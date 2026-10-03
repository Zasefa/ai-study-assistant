from pydantic import BaseModel


class StudyAnswer(BaseModel):
    topic: str
    definition: str
    how_it_works: str
    real_world_example: str
    interview_question: str