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

from app.vector_store import (
    get_retriever,
    search_with_scores
)

from app.document_processor import process_pdf

from app.memory import (
    get_history,
    add_message
)


# ==============================
# FASTAPI APP
# ==============================

app = FastAPI(
    title="AI Study Assistant",
    version="1.0"
)


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://ai-study-assistant-frontend-mxhd.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ==============================
# REQUEST MODELS
# ==============================

class Question(BaseModel):
    question: str


class PDFQuestion(BaseModel):
    question: str
    document_id: str
    session_id: str = "student1"


# ==============================
# HOME
# ==============================

@app.get("/")
def home():

    return {
        "message": "AI Study Assistant Backend Running 🚀"
    }


# ==============================
# ASK AI
# ==============================

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

        print(
            "\nASK AI ERROR:",
            type(e).__name__
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error_type": type(e).__name__,
                "message": str(e)
            }
        )


# ==============================
# GENERATE MCQ
# ==============================

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

        print(
            "\nMCQ ERROR:",
            type(e).__name__
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error_type": type(e).__name__,
                "message": str(e)
            }
        )


# ==============================
# UPLOAD PDF
# ==============================

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

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

        print(
            "\nPDF ERROR:",
            type(e).__name__
        )

        print(str(e))

        raise HTTPException(
            status_code=500,
            detail={
                "error_type": type(e).__name__,
                "message": str(e)
            }
        )


# ==============================
# ASK PDF
# ==============================

@app.post("/ask-pdf")
def ask_pdf(data: PDFQuestion):

    try:

        print("\n==============================")
        print("ASK PDF:", data.question)
        print("DOCUMENT:", data.document_id)
        print("==============================")


        # ==============================
        # CONVERSATION HISTORY
        # ==============================

        history_data = get_history(
            data.session_id
        )

        history = "\n".join(
            f"User: {item['question']}\n"
            f"Assistant: {item['answer']}"
            for item in history_data
        )


        # ==============================
        # ADAPTIVE RETRIEVAL
        # ==============================

        broad_keywords = [
            "main topic",
            "overview",
            "summary",
            "summarize",
            "whole document",
            "entire document",
            "document about",
            "main features",
            "key points",
            "explain the project",
            "project overview",
            "overall"
        ]

        question_lower = data.question.lower()

        is_broad_question = any(
            keyword in question_lower
            for keyword in broad_keywords
        )


        if is_broad_question:

            retrieval_k = 8

            print(
                "Broad question detected → "
                "retrieving 8 chunks"
            )

        else:

            retrieval_k = 3

            print(
                "Specific question detected → "
                "retrieving 3 chunks"
            )


        # ==============================
        # SEARCH WITH SIMILARITY SCORES
        # ==============================

        results = search_with_scores(
            query=data.question,
            k=retrieval_k,
            document_id=data.document_id
        )


        print(
            "Retrieved documents:",
            len(results)
        )


        # ==============================
        # SHOW SCORES
        # ==============================

        for i, (document, score) in enumerate(results):

            print(
                f"\n--- Retrieved Chunk {i + 1} ---"
            )

            print(
                "Similarity score:",
                score
            )

            print(
                "Page:",
                document.metadata.get("page")
            )

            print(
                "Content:"
            )

            print(
                document.page_content
            )


        # ==============================
        # NO RESULTS
        # ==============================

        if not results:

            return {
                "question":
                    data.question,

                "answer":
                    "I could not find this information "
                    "in the provided document.",

                "sources":
                    []
            }


        # ==============================
        # RELEVANCE CHECK
        # ==============================

        # Chroma distance:
        # Lower score = more similar
        #
        # We use a conservative threshold
        # for this first test.

        relevance_threshold = 1.0

        relevant_results = [
            (document, score)
            for document, score in results
            if score <= relevance_threshold
        ]


        print(
            "\nRelevant documents:",
            len(relevant_results)
        )


        # ==============================
        # NO RELEVANT INFORMATION
        # ==============================

        if not relevant_results:

            print(
                "No sufficiently relevant chunks found."
            )

            return {
                "question":
                    data.question,

                "answer":
                    "I could not find this information "
                    "in the provided document.",

                "sources":
                    []
            }


        # ==============================
        # CREATE CONTEXT
        # ==============================

        documents = [
            document
            for document, score
            in relevant_results
        ]


        context = "\n\n".join(
            document.page_content
            for document in documents
        )


        # ==============================
        # RAG PROMPT
        # ==============================

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
- If the answer is not present in the context, say:

"I could not find this information in
the provided document."

Give a clear and beginner-friendly answer.
"""


        # ==============================
        # GENERATE ANSWER
        # ==============================

        answer = generate_text(
            prompt
        )


        # ==============================
        # SAVE CONVERSATION
        # ==============================

        add_message(
            data.session_id,
            data.question,
            answer
        )


        # ==============================
        # CREATE SOURCES
        # ==============================

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


        # ==============================
        # REMOVE DUPLICATE PAGES
        # ==============================

        unique_sources = []

        seen_pages = set()

        for source in sources:

            page = source["page"]

            if page not in seen_pages:

                unique_sources.append(
                    source
                )

                seen_pages.add(
                    page
                )


        print("ASK PDF SUCCESS")


        # ==============================
        # RETURN RESPONSE
        # ==============================

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