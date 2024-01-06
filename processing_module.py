from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
class Response(BaseModel):
     processing_level: float

json_format = """
{
  "processing_level": float
}
"""

def get_processing_level(problem, solution, product):
  sys_msg = None
  business_problem = f""" {problem} """
  business_solution = f""" {solution} """
  prompt = f"""
You will be presented with a product name, business problem, and business solution for a business idea in the circular economy.
Based on the following evaluation criteria, assess the level of processing difficulty for the business solution. 
Use a scale of 0-1 to rate the difficulty, where closer to 0 (easy) implies a simpler breakdown process and closer to 1 (hard) implies a more complex industrial process.
Evaluation Criteria: 
1) Size: Assess the difficulty of processing based on the mass of the product. (EX: extremely heavy or bulky products (hard, closer to 1), light and small products (easy, closer to 0), washing machine (hard, closer to 1), ink cartridge (easy, closer to 0)) 
2) Chemical Toxicity: more hazardous materials are more difficult and expensive to process (EX: Non-toxic materials like paper (easy, closer to 0), Hazardous chemicals or radioactive materials (hard, closer to 1), advanced smartphones and laptops (hard, closer to 1)) 
3) Technology Needed: Rate the processing difficulty based on the level of technology required for processing (EX: Low-tech processing like manual labor (easy, closer to 0), High-tech processes involving specialized machinery (hard, closer to 1))

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
    get_processing_level(
      problem="The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.",
      solution="Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application.",
      product="Modular Construction"
    )
    get_processing_level(
      problem="The massive shift in student learning towards digital platforms has resulted in an increased carbon footprint due to energy consumption from data centers and e-waste from obsolete devices. Simultaneously, physical books are often produced, used once, and then discarded, leading to waste and deforestation.",
      solution="Implement a ""Book Swap"" program within educational institutions and local communities. This platform allows students to trade books they no longer need with others who require them, reducing the need for new book production and hence, lowering the rate of resource depletion. Furthermore, the platform could have a digital component to track book exchanges, giving users credits for each trade, which they can accrue and redeem. This system encourages and amplifies the benefits of reusing and sharing resources, thus contributing to the circular economy.   By integrating gamification, getting students and parents involved and providing an easy-to-use platform, the program could influence a cultural shift towards greater resource value appreciation and waste reduction. In terms of the financial aspect, less reliance on purchasing new books could save money for students, parents and schools.",
      product="Book Swap"  
    )