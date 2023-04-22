# chatgpt_querier
Fetches highlights from readwise.io, convert them into flashcards using ChatGPT, and send them to Anki for future review

# How to use

Anki must be running with the AnkiConnect plugin listening on default port `8765`.

```bash
OPENAI_API_KEY=XXX READWISE_API_KEY=YYY python main.py
```
