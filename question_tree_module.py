from product_module import get_product
from embedded_value_module import get_embedded_value
from access_module import get_access_level
from processing_module import get_processing_level

def ask_questions_in_tree(problem, solution):
  product_response = get_product(problem, solution)
  product = product_response.product
  print(("=" * 10) + " PRODUCT " + ("=" * 10))
  print(product)
  embedded_value_response = get_embedded_value(problem, solution, product)
  embedded_value = embedded_value_response.embedded_value
  print(("=" * 10) + " EMBEDDED VALUE " + ("=" * 10))
  print(embedded_value)
  access_level_response = get_access_level(problem, solution, product)
  access_level = access_level_response.access_level
  print(("=" * 10) + " ACCESS LEVEL " + ("=" * 10))
  print(access_level)
  processing_level_response = get_processing_level(problem, solution, product)
  processing_level = processing_level_response.processing_level
  print(("=" * 10) + " PROCESSING LEVEL " + ("=" * 10))
  print(processing_level)

  return product, embedded_value, access_level, processing_level 