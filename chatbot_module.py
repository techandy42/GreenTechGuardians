import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict

load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)

class Conversation:
  def __init__(self, background_info: str):
    self.background_info = background_info
    self.chat_history = []

  def ask_question(self, question: str) -> str:
    self.chat_history.append({"role": "user", "content": self.background_info + question})

    completion = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=self.chat_history
    )

    self.chat_history.append({"role": "assistant", "content": completion.choices[0].message.content})

    return completion.choices[0].message.content