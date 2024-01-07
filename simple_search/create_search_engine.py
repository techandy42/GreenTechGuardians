from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
import os
import pandas as pd

df = pd.read_json('outputs/combined_data_first_200_rows.jsonl', lines=True)

combined_list = df.apply(lambda row: f"{row['product']} {row['summary']} {' '.join(row['categories'])}", axis=1).tolist()

schema = Schema(title=TEXT(stored=True))

index_dir = "indexdir"
if not os.path.exists(index_dir):
    os.mkdir(index_dir)

# Create an index
index = create_in(index_dir, schema)

# Add documents to the index
writer = index.writer()
for string in combined_list:  # Assuming you have a list of strings
    writer.add_document(title=string)
writer.commit()
