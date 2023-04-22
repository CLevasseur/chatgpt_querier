# chatgpt_querier
Fetches highlights from readwise.io, convert them into flashcards using ChatGPT, and send them to Anki for future review

Those highlights are automatically synchronized from Kindle Highlights, and also created from web page content using the Readwise Highlighter browser extension.

# How to use

Anki must be running with the AnkiConnect plugin listening on default port `8765`.

```bash
OPENAI_API_KEY=XXX READWISE_API_KEY=YYY python main.py
```
