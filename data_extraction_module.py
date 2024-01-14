import pandas as pd
from question_tree_module import ask_questions_in_tree
import json

def get_last_index(jsonl_file_name):
  # Initialize a variable to store the last line
  last_line = None

  # Open the .jsonl file and read lines
  with open(jsonl_file_name, 'r') as file:
      for line in file:
          last_line = line.strip()

  # Convert the last JSON string to a Python dictionary
  if last_line:
      last_json_object = json.loads(last_line)
  else:
      last_json_object = None

  if last_json_object is None:
      raise Exception("No last JSON object found")
  else:
      return last_json_object['id']

def extract_data_from_csv_file(df, jsonl_file_name):
  added_index_list = []
  with open(jsonl_file_name, 'a') as file:
    for index, row in df.iterrows():
      try:
        product, summary, embedded_value, embedded_value_reasoning, access_level, access_level_reasoning, processing_level, processing_level_reasoning, categories, categories_reasoning = ask_questions_in_tree(row['problem'], row['solution'])
        last_index = get_last_index(jsonl_file_name)
        current_index = last_index + 1 + index
        added_index_list.append(current_index)
        data = {
          "id": current_index,
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

  return added_index_list

if __name__ == "__main__":
  df = pd.read_csv('AI_EarthHack_Dataset.csv', encoding='latin-1')
  df = df.iloc[:5]
  added_index_list = extract_data_from_csv_file(df, "./outputs/extracted_data_training_dataset.jsonl")
  print("added_index_list:")
  print(added_index_list)