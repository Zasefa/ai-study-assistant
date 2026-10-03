from typing import Dict, List


chat_sessions: Dict[str, List[dict]] = {}


def get_history(session_id: str):

    return chat_sessions.get(
        session_id,
        []
    )


def add_message(
    session_id: str,
    question: str,
    answer: str
):

    if session_id not in chat_sessions:

        chat_sessions[session_id] = []

    chat_sessions[session_id].append(
        {
            "question": question,
            "answer": answer
        }
    )