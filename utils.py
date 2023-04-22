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
    # we check if any deck name can be found in the answer, in which case we return it
    for deck_name in deck_list:
        if deck_name.lower() in chat_gpt_answer.lower():
            return deck_name

    # or we didn't find any of the exact deck names in the answer, defaults to difflib to find closest match
    matches = difflib.get_close_matches(chat_gpt_answer, deck_list, n=1)
    if len(matches) > 0:
        return matches[0]

    # we didn't find any match deck, will need to be set manually in Anki
    return "Default"
