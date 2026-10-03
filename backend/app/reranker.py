from app.llm import model


def rerank_documents(question, documents, top_k=3):

    if not documents:
        return []

    document_text = ""

    for i, document in enumerate(documents):

        document_text += f"""
DOCUMENT {i}

{document.page_content}

--------------------
"""

    prompt = f"""
You are a document relevance evaluator.

User question:
{question}

Below are retrieved documents.

{document_text}

Choose the {top_k} documents that are most useful
for answering the user's question.

Return ONLY the document numbers separated by commas.

Example:
2,0,5
"""

    response = model.invoke(prompt)

    try:
        selected_indexes = [
            int(index.strip())
            for index in response.content.split(",")
        ]
    except ValueError:
        return documents[:top_k]

    selected_documents = []

    for index in selected_indexes:

        if 0 <= index < len(documents):
            selected_documents.append(
                documents[index]
            )

    return selected_documents[:top_k]