import openai as openai


class ChatGPTContext:

    def __init__(self):
        self.messages = list()

    def ask_chat_gpt(self, question: str) -> str:
        self.messages.append({"role": "user", "content": question})
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        answer = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer
