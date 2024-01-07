import pandas as pd

original_dataset = pd.read_csv('AI_EarthHack_Dataset.csv', encoding='latin-1')
extracted_dataset = pd.read_json('outputs/extracted_data_first_200_rows.jsonl', lines=True)

for index, row in extracted_dataset.iterrows():
    extracted_dataset['problem'] = original_dataset['problem']
    extracted_dataset['solution'] = original_dataset['solution']

extracted_dataset.to_csv('outputs/combined_data_first_200_rows.csv', index=False)