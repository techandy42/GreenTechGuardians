import pandas as pd
from question_tree_module import ask_questions_in_tree
import json
import os
import streamlit as st

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
      return 0
  else:
      return last_json_object['id']

def check_and_create_file(file_path):
    """
    Check if a file exists at the given path, and if it doesn't exist, create it.
    
    :param file_path: Path of the file to check and create.
    """
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            # Create an empty file
            pass
        print(f"File created at {file_path}")
    else:
        print("File already exists.")

def extract_data_from_csv_file(df, jsonl_file_name):
  check_and_create_file(jsonl_file_name)

  added_items = []
  last_index = get_last_index(jsonl_file_name)
  item_index = 0
  with open(jsonl_file_name, 'a') as file:
    for index, row in df.iterrows():
      try:
        try:
           st.progress(int((index-last_index)/len(df.iterrows())*100))
        except:
           pass
        product, summary, embedded_value, embedded_value_reasoning, access_level, access_level_reasoning, processing_level, processing_level_reasoning, categories, categories_reasonings = ask_questions_in_tree(row['problem'], row['solution'])
        current_index = last_index + 1 + item_index
        item_index += 1
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
          "categories_reasonings": categories_reasonings,
          "problem": row["problem"],
          "solution": row["solution"],
        }
        added_items.append(data)
        json_data = json.dumps(data)
        file.write(json_data)
        file.write('\n')
        print("=" * 50)
        print(f"row {index} in dataframe: Processed item {current_index}...")
        print("=" * 50)
      except:
        print("=" * 50)
        print(f"row {index} in dataframe: Error while processing item {current_index}... Moving to next item...")
        print("=" * 50)
        continue
  print("hello")
  return added_items

if __name__ == "__main__":
  df = pd.read_csv('AI_EarthHack_Dataset.csv', encoding='latin-1')
  df = df.iloc[:5]
  added_items = extract_data_from_csv_file(df, "./outputs/extracted_data_training_dataset.jsonl")
  print("Added Items:")
  for item in added_items:
     print(f"- {item['id']}: {item['product']}")