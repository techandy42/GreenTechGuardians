from product_module import get_product
from summary_module import get_summary
from embedded_value_module import get_embedded_value
from access_module import get_access_level
from processing_module import get_processing_level
from categories_module import get_categories

def ask_questions_in_tree(problem, solution):
  product_response = get_product(problem, solution)
  product = product_response.product
  print(("=" * 10) + " PRODUCT " + ("=" * 10))
  print(product)
  summary_response = get_summary(problem, solution)
  summary = summary_response.summary
  print(("=" * 10) + " SUMMARY " + ("=" * 10))
  print(summary)
  embedded_value_response = get_embedded_value(product, summary, problem, solution)
  embedded_value = embedded_value_response.embedded_value
  embedded_value_reasoning = embedded_value_response.reasoning
  print(("=" * 10) + " EMBEDDED VALUE " + ("=" * 10))
  print(embedded_value)
  access_level_response = get_access_level(product, summary, problem, solution)
  access_level = access_level_response.access_level
  access_level_reasoning = access_level_response.reasoning
  print(("=" * 10) + " ACCESS LEVEL " + ("=" * 10))
  print(access_level)
  processing_level_response = get_processing_level(product, summary, problem, solution)
  processing_level = processing_level_response.processing_level
  processing_level_reasoning = processing_level_response.reasoning
  print(("=" * 10) + " PROCESSING LEVEL " + ("=" * 10))
  print(processing_level)
  categories_response = get_categories(product, summary, problem, solution)
  categories = categories_response.categories
  categories_reasoning = categories_response.reasoning
  print(("=" * 10) + " CATEGORIES " + ("=" * 10))
  print(categories)

  return product, summary, embedded_value, embedded_value_reasoning, access_level, access_level_reasoning, processing_level, processing_level_reasoning, categories, categories_reasoning

# Test Cases
if __name__ == "__main__":
  import json

  product, summary, embedded_value, embedded_value_reasoning, access_level, access_level_reasoning, processing_level, processing_level_reasoning, categories, categories_reasoning = ask_questions_in_tree(
    problem="The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.",
    solution="Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application."
  )
  
  data = {
    "product": product,
    "summary": summary,
    "embedded_value": embedded_value,
    "embedded_value_reasoning": embedded_value_reasoning,
    "access_level": access_level,
    "access_level_reasoning": access_level_reasoning,
    "processing_level": processing_level,
    "processing_level_reasoning": processing_level_reasoning,
    "categories": categories,
    "categories_reasoning": categories_reasoning
  }

  # Save experiment data
  with open('data.json', 'w') as outfile:
    json.dump(data, outfile)