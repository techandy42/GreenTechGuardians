import os
from dotenv import load_dotenv
import pinecone
from openai import OpenAI
import streamlit as st
import pandas as pd

load_dotenv()

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)

def get_embeddings(texts):
    response = client.embeddings.create(input=texts, model="text-similarity-babbage-001")
    return [embedding.embedding for embedding in response.data]

def search_index(query, index, top_k=10):
    query_embedding = get_embeddings([query])[0]
    query_results = index.query(queries=[query_embedding], top_k=top_k)
    print(query_results)
    ids = [int(match['id']) for match in query_results['results'][0]['matches']]
    return df[df['id'].isin(ids)]

df = pd.read_json('outputs/combined_data_first_200_rows.jsonl', lines=True)

print("=" * 10 + " Data Loaded " + "=" * 10)

pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')

index_name = 'greentechguardians'
index = pinecone.Index(index_name)

print("=" * 10 + " Pinecone Index Loaded " + "=" * 10)

st.title("Product Search")
query = st.text_input("Enter your search query:")

if query:
    results_df = search_index(query, index)
    for _, row in results_df.iterrows():
        st.write(f"ID: {row['id']}, Product: {row['product']}, Summary: {row['summary']}, Categories: {', '.join(row['categories'])}")

