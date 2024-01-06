import pandas as pd
from question_tree_module import ask_questions_in_tree
import json

df = pd.read_csv('AI_EarthHack_Dataset.csv', encoding='ISO-8859-1')

start_idx = 150
end_idx = 200

with open(f'extracted_data_row_{start_idx}_to_{end_idx}.jsonl', 'w') as file:
  for index, row in df.iloc[start_idx:end_idx].iterrows():
    try:
      product, summary, embedded_value, access_level, processing_level, categories = ask_questions_in_tree(row['problem'], row['solution'])
      data = {
        "id": row['id'],
        "product": product,
        "summary": summary,
        "embedded_value": embedded_value,
        "access_level": access_level,
        "processing_level": processing_level,
        "categories": categories
      }
      json_data = json.dumps(data)
      file.write(json_data)
      file.write('\n')
      print("=" * 50)
      print(f"{index}: Processed {row['id']}...")
      print("=" * 50)
    except:
      print("=" * 50)
      print(f"{index}: Error while processing {row['id']}... Moving to next item...")
      print("=" * 50)
      continue
