import pandas as pd
import json

# Read the original dataset
original_dataset = pd.read_csv('AI_EarthHack_Dataset.csv', encoding='latin-1')

# Read the extracted dataset
extracted_dataset = pd.read_json('outputs/extracted_data_first_200_rows.jsonl', lines=True)

# Assuming you want to add 'problem' and 'solution' columns to the extracted dataset
# from the original dataset. Make sure the length of both datasets is the same.
# If they are not the same, this step might throw an error or lead to incorrect data.
for index, row in extracted_dataset.iterrows():
    extracted_dataset['problem'] = original_dataset['problem']
    extracted_dataset['solution'] = original_dataset['solution']

# Save to a .jsonl file
with open(f'combined_data_first_200_rows.jsonl', 'w') as file:
    for index, row in extracted_dataset.iterrows():
        data = {
            "id": row['id'],
            "product": row['product'],
            "summary": row['summary'],
            "embedded_value": row['embedded_value'],
            "access_level": row['access_level'],
            "processing_level": row['processing_level'],
            "categories": row['categories'],
            "problem": row['problem'],
            "solution": row['solution']
        }
        json_data = json.dumps(data)
        file.write(json_data)
        file.write('\n')