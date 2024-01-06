from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
from product_module import get_product

class Response(BaseModel):
     embedded_value: float

json_format = """
{
  "embedded_value": float
}
"""

def get_embedded_value(problem, solution):
  product = get_product(problem, solution)
  sys_msg = None
  business_problem = f""" {problem} """
  business_solution = f""" {solution} """
  prompt = f"""
You will be presented with a product name in a circular economy business. Given the product name, rate the embedded value of the product based on the following criteria to provide a decimal number between 0 and 1, where 0 indicates low embedded value, 1 indicates high embedded value, and 0.5 indicates medium embedded value.
Rating criteria: 1) market price: the higher the market price for a unit of the product, the higher the embedded value (EX: industrial equipments (1), high-tech printers (0.6), diamond (1), paper (0), high fashion (0.6)) 2) maintenance: if maintenance of the product is expensive, the embedded value is high (EX: Xerox printers leased to corporations (0.8)) 3) Uniqueness: If the product contains cutting-edge technology, its embedded value is high (EX: software (0.8) 4) market demand: markets that have growing demand have products containing higher embedded value (EX: renewable energy sector products (0.6))

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
  get_embedded_value("The massive shift in student learning towards digital platforms has resulted in an increased carbon footprint due to energy consumption from data centers and e-waste from obsolete devices. Simultaneously, physical books are often produced, used once, and then discarded, leading to waste and deforestation.",
               "Implement a ""Book Swap"" program within educational institutions and local communities. This platform allows students to trade books they no longer need with others who require them, reducing the need for new book production and hence, lowering the rate of resource depletion. Furthermore, the platform could have a digital component to track book exchanges, giving users credits for each trade, which they can accrue and redeem. This system encourages and amplifies the benefits of reusing and sharing resources, thus contributing to the circular economy.   By integrating gamification, getting students and parents involved and providing an easy-to-use platform, the program could influence a cultural shift towards greater resource value appreciation and waste reduction. In terms of the financial aspect, less reliance on purchasing new books could save money for students, parents and schools.")
