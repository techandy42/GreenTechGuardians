import os
from dotenv import load_dotenv
from openai import OpenAI
from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
from typing import List

load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)
class Response(BaseModel):
     sample_questions: List[str]

json_format = """
{
  "sample_questions": List[str]
}
"""

class Conversation:
  def __init__(self, background_info: str):
    self.background_info = background_info
    self.chat_history = []

  def ask_question(self, question: str) -> str:
    self.chat_history.append({"role": "user", "content": question})

    completion = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[*self.chat_history, {"role": "user", "content": self.background_info}]
    )

    self.chat_history.append({"role": "assistant", "content": completion.choices[0].message.content})

    return completion.choices[0].message.content
  
  def get_sample_questions(self):
    sys_msg = None
    prompt = f"""
    You will be presented with a conversation between the user and a business advisory chatbot.
    Given the following question and answer between the user and the chatbot, please generate three sample questions that the user might ask next.
    The questions you generate should be relevant to green technology, circular economy, and business.
    If the question and answer are 'Nothing', then please generate three sample questions that directly asks about the current business, such as its business model and relevancy to green technology and circular economy.

    User Question:
    {self.chat_history[-2]['content'] if len(self.chat_history) >= 2 else 'Nothing'}

    Chatbot Answer:
    {self.chat_history[-1]['content'] if len(self.chat_history) >= 2 else 'Nothing'}
    """
    response = gpt_call(sys_msg, prompt, json_format)

    cleaned_response = clean_response(response)

    print(cleaned_response)
    
    validated_response = Response.model_validate_json(cleaned_response)

    print(validated_response)
    
    return validated_response
