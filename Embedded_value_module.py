from gpt_module import clean_response, gpt_call
from pydantic import BaseModel

class Response(BaseModel):
     product: str

json_format = """
{
  "embedded_value": str
}
"""

def get_embedded_value(problem, solution, product):
  sys_msg = None
  business_problem = f""" {problem} """
  business_solution = f""" {solution} """
  prompt = f"""
Given the following product name, as well as the business problem and solution, help me to assess the product embedded value based on factors such as market demand (EX: If the company is in the renewable energy sector, consider the growing demand for sustainable energy sources and how the main product aligns with this trend), Uniqueness (EX: If the company produces a cutting-edge technology, consider how it stands out from competitors and addresses specific market needs.), and Potential Growth of the product(EX: If the company is to evaluate software solutions, evaluate its adaptabilities in different industries and different area, and generate its potential trend in the near future).

Product Name:

{product}

As references, here are the original business problem and solution.

Business Problem:

{business_problem.strip()}

Business Solution:

{business_solution.strip()}
"""
  response = gpt_call(sys_msg, prompt, json_format)

  cleaned_response = clean_response(response)

#   print(cleaned_response)
  
  validated_response = Response.model_validate_json(cleaned_response)

#   print(validated_response)
  
  return validated_response
   

# Test Cases
if __name__ == "__main__":
   get_embedded_value("A startup company, TechInnovate, has developed a new augmented reality (AR) headset. The company seeks to understand the embedded value of this product in the market.", "TechInnovate is a technology startup that specializes in developing cutting-edge augmented reality solutions. Their latest product is an advanced AR headset designed for both consumer and enterprise applications. The headset boasts high-resolution displays, advanced gesture recognition, and seamless integration with various software applications.")