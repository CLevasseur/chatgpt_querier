import os
from dataclasses import dataclass

import requests as requests


class Readwise:

    def __init__(self):
        self.__token = os.environ["READWISE_API_KEY"]

    def fetch_from_export_api(self, updated_after=None):
        full_data = []
        next_page_cursor = None
        while True:
            params = {}
            if next_page_cursor:
                params['pageCursor'] = next_page_cursor
            if updated_after:
                params['updatedAfter'] = updated_after
            response = requests.get(
                url="https://readwise.io/api/v2/export/",
                params=params,
                headers={"Authorization": f"Token {self.__token}"}
            )
            full_data.extend(response.json()['results'])
            next_page_cursor = response.json().get('nextPageCursor')
            if not next_page_cursor:
                break
        return full_data


@dataclass
class Highlight:
    resource_title: str  # Book name, web page title...
    text: str
    readwise_id: str
    readwise_url: str

    @staticmethod
    def from_readwise_export(readwise_export):
        highlights = list()

        for resource in readwise_export:
            for highlight in resource["highlights"]:
                highlights.append(Highlight(resource["title"], highlight["text"], str(highlight["id"]), highlight["readwise_url"]))

        return highlights
