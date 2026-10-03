from langchain_core.prompts import PromptTemplate


study_prompt = PromptTemplate.from_template(
    """
You are an AI Study Assistant.

Explain the following topic in simple,
beginner-friendly language.

Topic:
{topic}

Follow this structure:

1. What is it?
2. How does it work?
3. Why is it used?
4. Real-world example
5. Interview question

Keep the explanation clear and suitable
for a college student.
"""
)


mcq_prompt = PromptTemplate.from_template(
    """
You are an AI Study Assistant.

Create exactly 5 multiple-choice questions
about the following topic.

Topic:
{topic}

Requirements:

- Exactly 5 questions.
- Every question must have exactly 4 options.
- There must be exactly one correct answer.
- Provide a short explanation.
- Questions should test understanding.
- Difficulty should be beginner/intermediate.
- Avoid duplicate questions.
"""
)