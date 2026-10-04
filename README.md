### AI Study Assistant

An AI-powered study assistant designed to help students understand technical concepts, practice MCQs, and learn directly from their own PDF study material.

The application combines **Generative AI, FastAPI, React, LangChain, and Retrieval-Augmented Generation (RAG)** to create an interactive learning experience.

### Live Demo

👉 **[AI Study Assistant - Live Demo](https://ai-study-assistant-frontend-mxhd.onrender.com)**

### Backend API

👉 **[FastAPI Backend](https://ai-study-assistant-r2pa.onrender.com)**

👉 **[API Documentation](https://ai-study-assistant-r2pa.onrender.com/docs)**


##  Features

### 1. Ask AI

Ask questions about technical or academic topics and get beginner-friendly explanations.

The AI response includes:

- Definition
- How it works
- Real-world example
- Interview question

This makes the application useful for both **learning concepts and preparing for technical interviews**.


### 2. AI MCQ Generator

Generate multiple-choice questions from any topic.

Features include:

- 5 MCQs per topic
- 4 options for each question
- Answer checking
- Correct/incorrect feedback
- Explanation for answers

This allows students to practice concepts immediately after learning them.


###  3. PDF Study Assistant

Upload a PDF containing study material and ask questions about its content.

The application uses a **Retrieval-Augmented Generation (RAG)** pipeline to find relevant information from the uploaded document before generating an answer.

### RAG Pipeline

```text
PDF
 ↓
Text Extraction
 ↓
Text Chunking
 ↓
Embeddings
 ↓
ChromaDB
 ↓
Similarity Search
 ↓
Relevant Context
 ↓
Groq LLM
 ↓
AI Generated Answer

```



### Project Architecture

```text
                    ┌─────────────────────┐
                    │   React Frontend    │
                    │      Vite + CSS     │
                    └──────────┬──────────┘
                               │
                               │ HTTP Requests
                               ▼
                    ┌─────────────────────┐
                    │   FastAPI Backend   │
                    │      Python         │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐        ┌─────────────────┐
        │   Groq LLM      │        │    ChromaDB     │
        │  AI Generation  │        │ Vector Database │
        └─────────────────┘        └────────┬────────┘
                                            │
                                            ▼
                                      PDF Documents

```



### Tech Stack

## Frontend
-React
-Vite
-Axios
-CSS

## Backend
-Python
-FastAPI
-Pydantic
-LangChain
-REST APIs

## Generative AI
-Groq API
-openai/gpt-oss-20b
--Structured AI outputs
-Prompt engineering

## RAG / Vector Database
-Retrieval-Augmented Generation (RAG)
-ChromaDB
-LangChain Chroma
-PDF processing
-Embeddings
-Semantic search

## Deployment
-Render
-GitHub


### How the Application Works
## Ask AI Flow

``` text
User enters question
        ↓
React frontend
        ↓
FastAPI `/ask` endpoint
        ↓
Prompt generation
        ↓
Groq LLM
        ↓
Structured response
        ↓
Frontend displays answer

```

## MCQ Generation Flow

``` text
User enters topic
        ↓
React frontend
        ↓
FastAPI `/generate-mcq`
        ↓
Groq LLM
        ↓
Structured MCQ response
        ↓
5 questions + options + answers
        ↓
User practices MCQs

```

### PDF RAG Flow

``` text
User uploads PDF
        ↓
PDF text extraction
        ↓
Text splitting
        ↓
Embeddings
        ↓
ChromaDB
        ↓
Similarity search
        ↓
Relevant document chunks
        ↓
Groq LLM
        ↓
Answer based on PDF

```

### Project Structure

``` text

ai-study-assistant/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── llm.py
│   │   ├── rag.py
│   │   ├── vector_store.py
│   │   ├── prompts.py
│   │   ├── schemas.py
│   │   └── mcq_schema.py
│   │
│   ├── documents/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```


### Run the Project Locally

## 1. Clone the Repository

-git clone https://github.com/Zasefa/ai-study-assistant.git
-cd ai-study-assistant

## 2. Backend Setup

Create a virtual environment:
python -m venv .venv

Activate it on Windows:
.\.venv\Scripts\Activate.ps1

Install dependencies:
pip install -r backend/requirements.txt


## 3. Configure Environment Variables

Create a .env file inside the backend folder.
GROQ_API_KEY=your_groq_api_key

## 4. Start the Backend

cd backend
uvicorn app.main:app --reload

The backend will run locally at:
http://127.0.0.1:8000

FastAPI documentation:
http://127.0.0.1:8000/docs

## 5. Start the Frontend

-Open another terminal:
-cd frontend
-npm install
-npm run dev


###  Deployment

##  Frontend:

``` text
React + Vite
        ↓
GitHub
        ↓
Render Static Site

```

## Backend

``` text

FastAPI
        ↓
GitHub
        ↓
Render Web Service
```

## AI

``` text
FastAPI
   ↓
Groq API
   ↓
LLM Response
```

### Key Concepts Used

This project helped me understand and implement:

-Large Language Models (LLMs)
-Generative AI
-Prompt Engineering
-Structured AI Outputs
-Retrieval-Augmented Generation (RAG)
-Text Chunking
-Embeddings
-Vector Databases
-Semantic Search
-PDF Document Processing
-LangChain
-FastAPI
-REST APIs
-React
-API Integration
-Environment Variables
-Git & GitHub
-Cloud Deployment




### What I Learned

Through this project, I learned how an AI-powered application works from frontend to backend and AI model integration.
The major things I practiced were:

-Connecting a React frontend with a FastAPI backend
-Working with LLM APIs
-Designing prompts for consistent AI responses
-Generating structured AI outputs
-Building a basic RAG pipeline
-Processing PDF documents
-Creating and querying vector databases
-Using LangChain components
-Building REST APIs with FastAPI
-Connecting frontend and backend APIs
-Managing environment variables
-Deploying a full-stack AI application
-Debugging CORS and deployment issues


### Future Improvements

Some improvements planned for future versions:

-User authentication
-Multiple PDF/document management
-Chat history
-Improved RAG retrieval
-Streaming AI responses
-Conversation-based study sessions
-Study progress tracking
-Better mobile responsiveness
-Voice-based questions
-Personalized learning recommendations


### Author

Zasefa
B.Tech Computer Science & Engineering (AI/ML)

GitHub:
👉 https://github.com/Zasefa
