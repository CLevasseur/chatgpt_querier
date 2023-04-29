import json
import re

import requests as requests

from readwise import Highlight


class Anki:

    def __init__(self):
        self.__anki_connect_endpoint = "http://localhost:8765"

    def get_deck_names(self):
        data = {
            "action": "deckNames",
            "version": 6,
        }
        # Send the request to AnkiConnect
        response = requests.post(self.__anki_connect_endpoint, json.dumps(data))
        # Check if the request was successful
        if response.status_code != 200:
            print("An error occurred:", response.text)

        return response.json()["result"]

    def add_flashcard(self, deck_name: str, front_text: str, back_text: str, highlight: Highlight):
        model_name = "Basic"  # Name of the note type you want to use
        resource_title_without_special_chars = re.sub(r'\W+', '', highlight.resource_title)
        # Construct the data for the request
        data = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": model_name,
                    "fields": {
                        "Front": front_text,
                        "Back": back_text
                    },
                    "options": {
                        "allowDuplicate": False
                    },
                    "tags": ["chatgpt", f"resource:{resource_title_without_special_chars}", f"readwise_highlight_id:{highlight.readwise_id}"]
                }
            }
        }
        # Send the request to AnkiConnect
        response = requests.post(self.__anki_connect_endpoint, json.dumps(data))
        # Check if the request was successful
        if response.status_code != 200:
            print("An error occurred:", response.text)

        return

    def sync(self):
        data = {
            "action": "sync",
            "version": 6,
        }
        # Send the request to AnkiConnect
        response = requests.post(self.__anki_connect_endpoint, json.dumps(data))
        # Check if the request was successful
        if response.status_code != 200:
            print("An error occurred:", response.text)

        return
