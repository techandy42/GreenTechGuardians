from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
from product_module import get_product
from typing import Literal

Levels = Literal["Easy", "Medium", "Hard", "easy", "medium", "hard"]

class Response(BaseModel):
     access: Levels

json_format = """
{
  "access_level": "Easy" or "Medium" or "Hard"
}
"""

def get_access(problem, solution):
  product = get_product(problem, solution)
  sys_msg = None
  business_problem = f""" {problem} """
  business_solution = f""" {solution} """
  prompt = f"""
You will be presented with a product name in a circular economy business. Given the name of the product and based on the following evaluation criteria, assess how difficult it is to gain access to the product. Use a scale of 'Easy', 'Medium', and 'Hard' to rate the difficulty, where 'Easy' implies a simpler retrieval process and 'Hard' implies a more complex and difficult retrieval process. Evaluation criteria: 1) Public participation: it is easier to retrieve a product if the public is enthusiastic to return or provide such product (EX: the public is willing to return plastic bottles in Norway (Easy)) 2) Infrastructure and accessibility: Straightforward and streamlined retrieval processes makes is easier to access the product (EX: recycling bins (Easy), washing machines (Hard), industrial equipment requiring infrastructural partnerships to retrieve (Hard), products located in remote or difficult-to-reach areas(Hard), wind turbines (Hard), products requiring specialized equipment or expertise to retrieve (Hard)) 3) Existence of secondary markets: products containing materials with higher resale value are harder to access (EX: construction equipment (Hard), carpets (Easy)).

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
   get_access("The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage."
               ,"Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application.")
   get_access("The massive shift in student learning towards digital platforms has resulted in an increased carbon footprint due to energy consumption from data centers and e-waste from obsolete devices. Simultaneously, physical books are often produced, used once, and then discarded, leading to waste and deforestation.",
               "Implement a ""Book Swap"" program within educational institutions and local communities. This platform allows students to trade books they no longer need with others who require them, reducing the need for new book production and hence, lowering the rate of resource depletion. Furthermore, the platform could have a digital component to track book exchanges, giving users credits for each trade, which they can accrue and redeem. This system encourages and amplifies the benefits of reusing and sharing resources, thus contributing to the circular economy.   By integrating gamification, getting students and parents involved and providing an easy-to-use platform, the program could influence a cultural shift towards greater resource value appreciation and waste reduction. In terms of the financial aspect, less reliance on purchasing new books could save money for students, parents and schools.")
