import os
import pprint
from datetime import timedelta, datetime
from typing import List

from anki import Anki
from chatgpt import ChatGPTContext
from readwise import Readwise, Highlight
from utils import parse_answer_as_flashcards, find_exact_deck_name


def convert_highlight_to_flashcards(anki: Anki, deck_names: List[str], highlight: Highlight):
    context = ChatGPTContext()

    if not highlight.note:
        question = highlight.text + "\n\nCan you make at most 2 questions out of this ?"
        _ = context.ask_chat_gpt(question)

        question = "Can you give a concise answer to those questions, formatted like 'Q:{question}\nA:{answer}' ? Don't write anything else."
        answer = context.ask_chat_gpt(question)
    else:
        question = highlight.text + "\n\n" + highlight.note
        if not (question.endswith("?") or question.endswith(".")):
            question += "."

        question += " Make flashcards, formatted like 'Q:{question}\nA:{answer}'. Name things explicitly. Do not use pronouns. Do not write anything else."
        answer = context.ask_chat_gpt(question)

    deck_question = f"What is the best deck for these flashcards ? Pick one of {', '.join(deck_names)}. Don't write anything else"
    deck_name = context.ask_chat_gpt(deck_question)
    exact_deck_name = find_exact_deck_name(deck_names, deck_name)
    pp = pprint.PrettyPrinter()
    pp.pprint(context.messages)
    print(f"Exact deck name is {exact_deck_name}")
    flashcards = parse_answer_as_flashcards(answer)
    pp.pprint(f"Parsed flashcards: {flashcards}")
    for (flashcard_question, flashcard_answer) in flashcards:
        anki.add_flashcard(exact_deck_name, flashcard_question, flashcard_answer, highlight)


if __name__ == "__main__":
    anki = Anki()
    deck_names = anki.get_deck_names()

    readwise = Readwise()
    readwise_export = readwise.fetch_from_export_api(datetime.now() - timedelta(days=30))

    highlights = Highlight.from_readwise_export(readwise_export)

    already_processed_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "already_processed.txt")
    already_processed = set()
    if os.path.exists(already_processed_filepath):
        with open(already_processed_filepath, "r") as f:
            already_processed = set(f.read().splitlines())

    new_highlights = False

    for highlight in highlights:
        if highlight.readwise_id in already_processed:
            continue

        new_highlights = True
        print("Processing highlight %s (%s)" % (highlight.readwise_id, highlight.readwise_url))
        convert_highlight_to_flashcards(anki, deck_names, highlight)

        with open(already_processed_filepath, "a") as f:
            f.write(highlight.readwise_id + "\n")

    if new_highlights:
        anki.sync()
        print(f"Successfully synced with remote database")


