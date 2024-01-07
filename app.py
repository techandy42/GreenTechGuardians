import os
from dotenv import load_dotenv
import pinecone
from openai import OpenAI
import streamlit as st
import pandas as pd
from individual_report_app import report

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

index_name = 'green'
index = pinecone.Index(index_name)

print("=" * 10 + " Pinecone Index Loaded " + "=" * 10)

if 'view_state' not in st.session_state:
    st.session_state.view_state = 'search'  # Possible values: 'search', 'report'

def view_report(item_id):
    # Function to view report and change state
    st.session_state.view_state = 'report'
    st.session_state.selected_item_id = item_id
    st.experimental_rerun()

def go_back():
    # Function to go back to the search view
    st.session_state.view_state = 'search'
    st.experimental_rerun()
# Main App

if st.session_state.view_state == 'search':
    st.title("GreenTechGuardians Business Search Engine")
    query = st.text_input("Enter your search query:")
    if query:
        results_df = search_index(query, index)
        for _, row in results_df.iterrows():
            if st.button(f"ID: {row['id']}, Product: {row['product']}, Summary: {row['summary']}, Categories: {', '.join(row['categories'])}"):
                view_report(row['id'])  # Update state and view report

elif st.session_state.view_state == 'report':
    # Clear the previous items and show the report
    st.empty()
    if st.button("Go Back To Search"):
        go_back()  # Go back to search view
    report(st.session_state.selected_item_id)
    similar_results_df = search_index(df[df['id']==st.session_state.selected_item_id].iloc[0]['summary'], index)
    st.subheader("Similar Businesses")
    for _, row in similar_results_df.iterrows():
        if st.button(f"ID: {row['id']}, Product: {row['product']}, Summary: {row['summary']}, Categories: {', '.join(row['categories'])}"):
            view_report(row['id'])  # Update state and view report