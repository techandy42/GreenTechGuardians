from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
class Response(BaseModel):
     category_reasoning: str

json_format = """
{
  "category_reasoning": str
}
"""
def get_category_reason(problem, solution, category):
     business_problem = f""" {problem} """
     business_solution = f""" {solution} """
     prompt = f"""Given the following business problem in a circular economy, a corresponding business solution, and the category of that business solution, explain in 25 words why the business solution would have received that category. The rating was given by the following criteria: 
Choose ONLY from the following list: - RPO (Retain Product Ownership) (The business rents or leases a product rather than selling it) - PLE (Product Life Extension) (The business designs the product to last longer) - DFR (Design For Recycling) (The business redesigns its product or manufacturing process to allow recyclability of reusability of the materials involved) - PARTNERSHIP (Partnering with other organizations) (The business collaborates with other organizations to achieve its goals). For example, given a problem description: “The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage”, and the corresponding business solution: “Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application”, the correct tag is DFR. Other examples: book swapping program (RPO), Servicing and repairing commercial tires (PLE)

     Business Problem:

     {business_problem.strip()}

     Business Solution:

     {business_solution.strip()}

     Business Strategy Category:
     {str(category).strip()}
     """
     response = gpt_call(None, prompt, json_format)
     cleaned_response = clean_response(response)
     # print(cleaned_response)
     validated_response = Response.model_validate_json(cleaned_response)
     # print(validated_response)
     return validated_response