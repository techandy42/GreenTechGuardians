import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Optional, Dict
import re

load_dotenv()

client = OpenAI(
  api_key=os.environ.get("OPENAI_API_KEY")
)

# Finding and extracting the JSON content; ignores all string that comes before and after the ```json <JSON> ``` marker
def clean_response(response: str):
  pattern = r"```json\n(.*?)\n```"

  match = re.search(pattern, response, flags=re.DOTALL)

  if match:
      cleaned_response = match.group(1)
      return cleaned_response
  else:
      raise Exception("No JSON content found in response")

def gpt_call(sys_msg: Optional[str], prompt: str, json_format: Dict) -> str:
  format_specification = f"""
I will ask you questions and you will respond. Your response should be in JSON format, with the following structure.:
```json
{json_format.strip()}
```
"""

  print(format_specification + prompt)

  messages = []

  if sys_msg is not None:
    messages.append({"role": "system", "content": sys_msg})

  messages.append({"role": "user", "content": format_specification + prompt})

  completion = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=messages
  )

  print(completion.choices[0].message.content)

  return completion.choices[0].message.content

from pydantic import BaseModel

class ScoreResponse(BaseModel):
     product: str

json_format = """
{
  "product": str
}
"""

def get_Embedded_Value(problem, solution):
  sys_msg = None
  business_problem = f""" {problem} """
  business_solution = f""" {solution} """
  prompt = f"""
Given the description of a business, tokenize the description to identify the main product of the company and generate the main product. Then help me to assess the product embedded value based on factors.

Business Problem:

{business_problem.strip()}

Business Solution:

{business_solution.strip()}
"""
  response = gpt_call(sys_msg, prompt, json_format)

  cleaned_response = clean_response(response)

#   print(cleaned_response)
  
  validated_response = ScoreResponse.model_validate_json(cleaned_response)

#   print(validated_response)
  
  return validated_response
   

# Test Cases
if __name__ == "__main__":
   get_Embedded_Value("A startup company, TechInnovate, has developed a new augmented reality (AR) headset. The company seeks to understand the embedded value of this product in the market.", "TechInnovate is a technology startup that specializes in developing cutting-edge augmented reality solutions. Their latest product is an advanced AR headset designed for both consumer and enterprise applications. The headset boasts high-resolution displays, advanced gesture recognition, and seamless integration with various software applications.")