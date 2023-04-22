import difflib
from typing import List, Tuple


def parse_answer_as_flashcards(chat_gpt_answer: str) -> List[Tuple[str, str]]:
    result = list()

    question = None

    for line in chat_gpt_answer.splitlines():
        if question is None and line.startswith("Q:") or line.startswith("Question:"):
            question = line.rsplit(":", 1)[1]
        if question is not None and line.startswith("A:") or line.startswith("Answer:"):
            answer = line.rsplit(":", 1)[1]
            result.append((question, answer))
            question = None

    return result


def find_exact_deck_name(deck_list: List[str], chat_gpt_answer: str) -> str:
    matches = difflib.get_close_matches(chat_gpt_answer, deck_list, n=1)
    if len(matches) > 0:
        return matches[0]

    return "Default"
