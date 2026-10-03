# 🎓 AI Study Assistant

An AI-powered study assistant that helps students understand concepts, practice with MCQs, and learn directly from their PDF notes.

The project uses a React frontend, FastAPI backend, LangChain, Ollama for local AI inference, and ChromaDB for PDF-based RAG.

## 🚀 Live Demo

🔗 **Live Project:** Coming Soon

> The project currently runs locally using Ollama because the AI model is hosted on the user's computer.

## 📌 Features

### 🤖 Ask AI
Ask questions about technical or academic topics and receive beginner-friendly explanations.

The AI provides:
- Definition
- How it works
- Real-world example
- Interview question

### 📝 AI MCQ Generator

Enter a topic and generate 5 multiple-choice questions.

Features:
- 4 options per question
- Answer checking
- Correct/incorrect feedback
- Explanation for each answer

### 📚 PDF Study Assistant

Upload your study material in PDF format and ask questions about it.

The system:
1. Extracts text from the PDF
2. Splits the text into smaller chunks
3. Creates embeddings
4. Stores embeddings in ChromaDB
5. Retrieves relevant chunks
6. Sends the retrieved context to the local LLM
7. Generates an answer based on the PDF

### 🔎 RAG-Based Question Answering

The PDF feature uses Retrieval-Augmented Generation (RAG).

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
Retriever
 ↓
Relevant Context
 ↓
Ollama LLM
 ↓
Answer
