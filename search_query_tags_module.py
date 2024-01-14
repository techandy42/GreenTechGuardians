from gpt_module import clean_response, gpt_call
from pydantic import BaseModel
from typing import List

class Response(BaseModel):
     tags: List[str]

json_format = """
{
  "tags": List[str]
}
"""
def get_search_query_tags(query: str):
     prompt = f"""
Given the following search query, can you generate a list of tags that highlights the main concepts of the query?

For example, given search query "Green tech energy companies working on renewable resources", you should return:

```json
{{
     "tags": ["green-energy", "technology", "renewable-resources"]
}}
```

Search Query:
{query}
     """
     response = gpt_call(None, prompt, json_format)
     cleaned_response = clean_response(response)
     # print(cleaned_response)
     validated_response = Response.model_validate_json(cleaned_response)
     # print(validated_response)
     return validated_response