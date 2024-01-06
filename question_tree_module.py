from product_module import get_product
from embedded_value_module import get_embedded_value

def ask_questions_in_tree(problem, solution):
  product_response = get_product(problem, solution)
  product = product_response.product
  print(("=" * 10) + "PRODUCT" + ("=" * 10))
  print(product)
  embedded_value_response = get_embedded_value(problem, solution, product)
  embedded_value = embedded_value_response.embedded_value