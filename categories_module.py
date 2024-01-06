from gpt_module import clean_response, gpt_call
from pydantic import BaseModel, validator
from typing import List

class Response(BaseModel):
    categories: List[str]

    @validator('categories', each_item=True)
    def check_allowed_values(cls, v):
        allowed_values = {"DFR", "RPO", "PLE", "PARTNERSHIP"}
        if v not in allowed_values:
            raise ValueError(f"{v} is not a valid category")
        return v

json_format = """
{
  "categories": ["DFR", "RPO", "PLE", "PARTNERSHIP"]
}
"""

def get_categories(problem, solution, product):
  sys_msg = None
  business_problem = f""" {problem} """
  business_solution = f""" {solution} """
  prompt = f"""
You will be presented with a product name, business problem, and business solution for a business idea in the circular economy.
Your job is to provide one or more tags from the following list for the business solution: 
- RPO (Retain Product Ownership) (The business rents or leases a product rather than selling it) 
- PLE (Product Life Extension) (The business designs the product to last longer) 
- DFR (Design For Recycling) (The business redesigns its product or manufacturing process to allow recyclability of reusability of the materials involved)
- PARTNERSHIP (Partnering with other organizations) (The business collaborates with other organizations to achieve its goals)

For example, given a problem description: "The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage", and the corresponding business solution: "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application", the correct tag is DFR. Other examples: book swapping program (RPO), Servicing and repairing commercial tires (PLE)

Product Name:
{product}

Business Problem:

{business_problem.strip()}

Business Solution:

{business_solution.strip()}

"""
  response = gpt_call(sys_msg, prompt, json_format)

  cleaned_response = clean_response(response)

  print(cleaned_response)
  
  validated_response = Response.model_validate_json(cleaned_response)

  print(validated_response)
  
  return validated_response
   

# Test Cases
if __name__ == "__main__":
    get_categories(
      problem="The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.",
      solution="Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application.",
      product="Modular Construction"
    )
    get_categories(
      problem="The massive shift in student learning towards digital platforms has resulted in an increased carbon footprint due to energy consumption from data centers and e-waste from obsolete devices. Simultaneously, physical books are often produced, used once, and then discarded, leading to waste and deforestation.",
      solution="Implement a ""Book Swap"" program within educational institutions and local communities. This platform allows students to trade books they no longer need with others who require them, reducing the need for new book production and hence, lowering the rate of resource depletion. Furthermore, the platform could have a digital component to track book exchanges, giving users credits for each trade, which they can accrue and redeem. This system encourages and amplifies the benefits of reusing and sharing resources, thus contributing to the circular economy.   By integrating gamification, getting students and parents involved and providing an easy-to-use platform, the program could influence a cultural shift towards greater resource value appreciation and waste reduction. In terms of the financial aspect, less reliance on purchasing new books could save money for students, parents and schools.",
      product="Book Swap"  
    )