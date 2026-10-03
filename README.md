#  AI Study Assistant

An AI-powered study assistant that helps students understand concepts, practice with MCQs, and learn directly from their PDF notes.

The project uses a React frontend, FastAPI backend, LangChain, Ollama for local AI inference, and ChromaDB for PDF-based RAG.

## 📌 Features

###  Ask AI
Ask questions about technical or academic topics and receive beginner-friendly explanations.

The AI provides:
- Definition
- How it works
- Real-world example
- Interview question

###  AI MCQ Generator

Enter a topic and generate 5 multiple-choice questions.

Features:
- 4 options per question
- Answer checking
- Correct/incorrect feedback
- Explanation for each answer

###  PDF Study Assistant

Upload your study material in PDF format and ask questions about it.

The system:
1. Extracts text from the PDF
2. Splits the text into smaller chunks
3. Creates embeddings
4. Stores embeddings in ChromaDB
5. Retrieves relevant chunks
6. Sends the retrieved context to the local LLM
7. Generates an answer based on the PDF

## Tech Stack
### Frontend -
React
Vite
Axios
CSS

### Backend-
Python
FastAPI
LangChain
Pydantic

### AI -
Ollama
Llama 3.1 8B
Nomic Embed Text

### RAG / Vector Database -
ChromaDB
LangChain Chroma
PDF processing with PyPDF

## What I Learned -

Through this project, I worked with:

LLM integration
Prompt engineering
Structured AI outputs
Retrieval-Augmented Generation (RAG)
Text chunking
Embeddings
Vector databases
Semantic search
PDF document processing
FastAPI
React
REST APIs
Local LLM deployment with Ollama

## Future Improvements -
User authentication
Multiple document management
Chat history
Better document retrieval
Streaming AI responses
Cloud deployment
Mobile responsive improvements
Voice-based questions
Study progress tracking
