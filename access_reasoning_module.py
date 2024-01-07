from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
class Response(BaseModel):
     access_reasoning: str

json_format = """
{
  "access_reasoning": str
}
"""
def get_access_reason(problem, solution, access_level):
     business_problem = f""" {problem} """
     business_solution = f""" {solution} """
     prompt = f"""Given the following business problem in a circular economy, a corresponding business solution, and rating for access level, explain in 25 words why the solution would have received that rating for access level. The rating was given by the following criteria:
Based on the following evaluation criteria, assess how difficult it is to gain access to the product. Use a scale between 0 to 1 to rate the difficulty, where closer to 0 (easy) implies a simpler retrieval process and closer to 1 (hard) implies a more complex and difficult retrieval process.
Evaluation criteria:
1) Public participation: it is easier to retrieve a product if the public is enthusiastic to return or provide such product
(EX: if the product is water bottle recycling in Norway, and if Norwegian citizens are more willing to recycle water bottles, then the score will lean closer to 0)
2) Infrastructure and accessibility: Straightforward and streamlined retrieval processes makes is easier to access the product
(EX: recycling bins (easy, closer to 0), washing machines (hard, closer to 1), industrial equipment requiring infrastructural partnerships to retrieve (hard, closer to 1), products located in remote or difficult-to-reach areas (hard, closer to 1), wind turbines (hard, closer to 1), products requiring specialized equipment or expertise to retrieve (hard, closer to 1)) 3) Existence of secondary markets: products containing materials with higher resale value are harder to access (EX: construction equipment (hard, closer to 1), carpets (easy, closer to 0)).

     Business Problem:

     {business_problem.strip()}

     Business Solution:

     {business_solution.strip()}

     Access Level:
     {str(access_level).strip()}
     """
     response = gpt_call(None, prompt, json_format)
     cleaned_response = clean_response(response)
     # print(cleaned_response)
     validated_response = Response.model_validate_json(cleaned_response)
     # print(validated_response)
     return validated_response