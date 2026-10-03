from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import os
import shutil
import uuid

from app.llm import (
    generate_study_answer,
    generate_mcqs,
    generate_text
)

from app.prompts import (
    study_prompt,
    mcq_prompt
)

from app.vector_store import get_retriever
from app.document_processor import process_pdf
from app.memory import (
    get_history,
    add_message
)


app = FastAPI(
    title="AI Study Assistant",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# --------------------------------
# REQUEST MODEL
# --------------------------------

class Question(BaseModel):

    question: str


# --------------------------------
# HOME
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "AI Study Assistant Backend Running 🚀"
    }


# --------------------------------
# NORMAL AI QUESTION
# --------------------------------

@app.post("/ask")
def ask(data: Question):

    try:

        print("\n==============================")
        print("ASK AI:", data.question)
        print("==============================")

        prompt = study_prompt.format(
            topic=data.question
        )

        response = generate_study_answer(prompt)

        print("ASK AI SUCCESS")

        return {
            "question": data.question,
            "answer": response.model_dump()
        }

    except Exception as e:

        print("\nASK AI ERROR:", type(e).__name__)
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error_type": type(e).__name__,
                "message": str(e)
            }
        )


# --------------------------------
# MCQ GENERATOR
# --------------------------------

@app.post("/generate-mcq")
def generate_mcq(data: Question):

    try:

        print("\n==============================")
        print("GENERATE MCQ:", data.question)
        print("==============================")

        prompt = mcq_prompt.format(
            topic=data.question
        )

        response = generate_mcqs(prompt)

        print("MCQ SUCCESS")

        return response.model_dump()

    except Exception as e:

        print("\nMCQ ERROR:", type(e).__name__)
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error_type": type(e).__name__,
                "message": str(e)
            }
        )


# --------------------------------
# PDF UPLOAD
# --------------------------------

@app.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    try:

        print("\n==============================")
        print("PDF UPLOAD:", file.filename)
        print("==============================")

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="No file selected."
            )

        if not file.filename.lower().endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        os.makedirs(
            "documents",
            exist_ok=True
        )

        unique_filename = (
            f"{uuid.uuid4()}_{file.filename}"
        )

        file_path = os.path.join(
            "documents",
            unique_filename
        )

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        document_id = str(
            uuid.uuid4()
        )

        result = process_pdf(
            file_path,
            document_id
        )

        print("PDF SUCCESS")

        return {

            "message":
                "PDF uploaded and processed successfully.",

            "filename":
                file.filename,

            "document_id":
                document_id,

            "pages":
                result["pages"],

            "chunks":
                result["chunks"]
        }

    except HTTPException:

        raise

    except Exception as e:

        print("\nPDF ERROR:", type(e).__name__)
        print(str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error_type": type(e).__name__,
                "message": str(e)
            }
        )


# --------------------------------
# ASK PDF
# --------------------------------

class PDFQuestion(BaseModel):

    question: str
    document_id: str
    session_id: str = "student1"


@app.post("/ask-pdf")
def ask_pdf(data: PDFQuestion):

    try:

        print("\n==============================")
        print("ASK PDF:", data.question)
        print("DOCUMENT:", data.document_id)
        print("==============================")

        history_data = get_history(
            data.session_id
        )

        history = "\n".join(

            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}"

            for item in history_data
        )

        retriever = get_retriever(
            k=3,
            document_id=data.document_id
        )

        documents = retriever.invoke(
            data.question
        )

        print(
            "Retrieved documents:",
            len(documents)
        )

        if not documents:

            return {

                "question":
                    data.question,

                "answer":
                    "I could not find this information "
                    "in the provided document.",

                "sources": []
            }

        context = "\n\n".join(

            document.page_content

            for document in documents
        )

        prompt = f"""
You are an AI Study Assistant.

Answer the user's question using ONLY
the provided document context.

Conversation History:

{history}

Document Context:

{context}

Current Question:

{data.question}

Rules:

- Use only the provided document context.
- Do not use outside knowledge.
- Do not invent information.
- If the answer is not present, say:

"I could not find this information in
the provided document."

Give a clear and beginner-friendly answer.
"""

        answer = generate_text(prompt)

        add_message(
            data.session_id,
            data.question,
            answer
        )

        sources = []

        for document in documents:

            page = document.metadata.get(
                "page"
            )

            if page is not None:

                sources.append(
                    {
                        "page": page + 1
                    }
                )

        unique_sources = []

        seen_pages = set()

        for source in sources:

            page = source["page"]

            if page not in seen_pages:

                unique_sources.append(
                    source
                )

                seen_pages.add(page)

        print("ASK PDF SUCCESS")

        return {

            "question":
                data.question,

            "session_id":
                data.session_id,

            "document_id":
                data.document_id,

            "answer":
                answer,

            "sources":
                unique_sources
        }

    except Exception as e:

        print(
            "\nASK PDF ERROR:",
            type(e).__name__
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error_type":
                    type(e).__name__,

                "message":
                    str(e)
            }
        )