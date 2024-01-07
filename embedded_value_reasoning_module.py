from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
class Response(BaseModel):
     embedded_value_reasoning: str

json_format = """
{
  "embedded_value_reasoning": str
}
"""
def get_embedded_value_reason(problem, solution, embedded_value, product):
     business_problem = f""" {problem} """
     business_solution = f""" {solution} """
     prompt = f"""Given the following business problem in a circular economy, a corresponding business solution, the main business product, and the rating for embedded value of the main product, explain in 25 words why the product would have received that rating for embedded value. The rating was given by the following criteria:
Given the product name, rate the embedded value of the product based on the following criteria to provide a decimal number between 0 and 1, where 0 indicates low embedded value, 1 indicates high embedded value, and 0.5 indicates medium embedded value.
Rating criteria: 1) market price: the higher the market price for a unit of the product, the higher the embedded value (EX: industrial equipments (1), high-tech printers (0.6), diamond (1), paper (0), high fashion (0.6)) 2) maintenance: if maintenance of the product is expensive, the embedded value is high (EX: Xerox printers leased to corporations (0.8)) 3) Uniqueness: If the product contains cutting-edge technology, its embedded value is high (EX: software (0.8) 4) market demand: markets that have growing demand have products containing higher embedded value (EX: renewable energy sector products (0.6))

     Business Problem:

     {business_problem.strip()}

     Business Solution:

     {business_solution.strip()}

     Embedded Value Rating:
     {str(embedded_value).strip()}

     Main Product:
     {str(product).strip()}
     """
     response = gpt_call(None, prompt, json_format)
     cleaned_response = clean_response(response)
     # print(cleaned_response)
     validated_response = Response.model_validate_json(cleaned_response)
     # print(validated_response)
     return validated_response