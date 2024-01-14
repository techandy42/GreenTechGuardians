from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
class Response(BaseModel):
     processing_reasoning: str

json_format = """
{
  "processing_reasoning": str
}
"""
def get_processing_reason(problem, solution, processing_level):
     business_problem = f""" {problem} """
     business_solution = f""" {solution} """
     prompt = f"""Given the following business problem in circular economy, a corresponding business solution, and rating for processing level, explain in 25 words why the solution
     would have received that rating for processing level. The rating was given by the following criteria: 
     Based on the following evaluation criteria, assess the level of processing difficulty for the business solution. 
     Use a scale of 0-1 to rate the difficulty, where closer to 0 (easy) implies a simpler breakdown process and closer to 1 (hard) implies a more complex industrial process.
     Evaluation Criteria: 
     1) Size: Assess the difficulty of processing based on the mass of the product. (EX: extremely heavy or bulky products (hard, closer to 1), light and small products (easy, closer to 0), washing machine (hard, closer to 1), ink cartridge (easy, closer to 0)) 
     2) Chemical Toxicity: more hazardous materials are more difficult and expensive to process (EX: Non-toxic materials like paper (easy, closer to 0), Hazardous chemicals or radioactive materials (hard, closer to 1), advanced smartphones and laptops (hard, closer to 1)) 
     3) Technology Needed: Rate the processing difficulty based on the level of technology required for processing (EX: Low-tech processing like manual labor (easy, closer to 0), High-tech processes involving specialized machinery (hard, closer to 1)).

     Business Problem:

     {business_problem.strip()}

     Business Solution:

     {business_solution.strip()}

     Processing Level:
     {str(processing_level).strip()}
     """
     response = gpt_call(None, prompt, json_format)
     cleaned_response = clean_response(response)
     # print(cleaned_response)
     validated_response = Response.model_validate_json(cleaned_response)
     # print(validated_response)
     return validated_response