import streamlit as st
import pandas as pd
from circular_matrix import plot_matrix, get_suggestion
from clustering_test import cluster_assignment, clusters
from comparing_similarities import get_percentiles_for_business, get_modified_percentile
from clustering_test import clustering_model
from dotenv import load_dotenv
import pinecone
import os
from solution_rating import percentile_score, strategy_score, ind_score_overall

load_dotenv()
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')
index_name = 'greentechguardians'
index = pinecone.Index(index_name)

if 'processing_rating' not in st.session_state:
    st.session_state.processing_rating = None
if 'access_rating' not in st.session_state:
    st.session_state.access_rating = None
if 'embedded_value_rating' not in st.session_state:
    st.session_state.embedded_value_rating = None
if 'processing_reasoning' not in st.session_state:
    st.session_state.processing_reasoning = None
if 'access_reasoning' not in st.session_state:
    st.session_state.access_reasoning= None
if 'embedded_value_reasoning' not in st.session_state:
    st.session_state.embedded_value_reasoning = None
if 'processing_percentile' not in st.session_state:
    st.session_state.processing_percentile = None
if 'access_percentile' not in st.session_state:
    st.session_state.access_percentile = None
if 'embedded_value_percentile' not in st.session_state:
    st.session_state.embedded_value_percentile = None

if 'edited' not in st.session_state:
     st.session_state.edited = {}
if 'overall_score' not in st.session_state:
     st.session_state.overall_score = None


df = pd.read_json('outputs/extracted_data_training_dataset.jsonl', lines=True)
strat_descriptions = {"RPO":"Retain Product Ownership: Producer rents or leases rather than selling the product.",
                      "DFR":"Design for Recycling: The company redesigns the product or its manufacturing and related processes to maximize recoverability of the materials involved.",
                      "PLE": "Product Life Extension: The company produces its product to last longer either by design or by providing related services.",
                      "PARTNERSHIP": "Partnering specific technological expertise or organizations to increase efficiency and reduce wastage"
                      }
strat_full_names = {"RPO": "RPO (Retain Product Ownership)",
                    "DFR": "DFR (Design for Recycling)",
                    "PLE": "PLE (Product Life Extension)",
                    "PARTNERSHIP": "PARTNERSHIP"}

def add_to_edited(id, content_type, content):
     if id not in st.session_state.edited.keys():
          st.session_state.edited[id] = {}
     st.session_state.edited[id][content_type] = content
     print(st.session_state.edited)



def report(id):
     business = df[df['id']==id].iloc[0]
     st.title(business['product'])
     st.header("Problem Statement")
     st.write(business['problem'])
     st.header("Solution")
     st.write(business['summary'])
     with st.expander("More Detailed Description"):
          st.write(business['solution'])
     if not st.session_state.overall_score:
          st.session_state.overall_score = strategy_score[id+1]
     overall_score_placeholder = st.empty()
     overall_score_placeholder.subheader(f"Overall Solution Score: {st.session_state.overall_score}/10")
     # columns = st.columns(3)
     percentiles = get_percentiles_for_business(id, df, cluster_assignment, clustering_model, index)

     ### PROCESSING LEVEL SECTION ###

     st.subheader("Processing Level")
     st.write(f"How hard is it to process the relevant materials for this {business['product']}?")

     if not st.session_state.processing_rating:
          st.session_state.processing_rating = round(business['processing_level'],2)
     processing_rating_placeholder = st.empty()
     processing_rating_placeholder.write(st.session_state.processing_rating)

     if not st.session_state.processing_percentile:
          st.session_state.processing_percentile = round(percentiles['business_processing_percentile'],2)
     processing_percentile_placeholder = st.empty()
     processing_percentile_placeholder.write(f"This business is at the {st.session_state.processing_percentile}th percentile of similar businesses")

     with st.expander("See reasoning"):
          if not st.session_state.processing_reasoning:
               st.session_state.processing_reasoning = business['processing_level_reasoning']
          processing_reasoning_placeholder = st.empty()
          processing_reasoning_placeholder.write(st.session_state.processing_reasoning)

     with st.expander("I would like to modify this section"):
          with st.form("Edit Processing Level"):
               st.write("Please enter your desired content. Leave an item blank if you'd like to keep the original content.")
               processing_input = st.number_input("Enter new rating", placeholder="Enter")
               if processing_input <= 1 and processing_input >= 0:
                    st.session_state.processing_rating = processing_input
                    add_to_edited(id, 'processing_level', processing_input)
               else:
                    st.write("Sorry! The input must be between 0 and 1")
               processing_reasoning_input = st.text_input("Enter new reasoning", placeholder = "Enter")
               if processing_reasoning_input != "":
                    st.session_state.processing_reasoning = processing_reasoning_input
               submitted = st.form_submit_button("Submit")
               if submitted:
                    processing_rating_placeholder.empty()
                    processing_rating_placeholder.write(round(st.session_state.processing_rating,2))
                    processing_reasoning_placeholder.empty()
                    processing_reasoning_placeholder.write(st.session_state.processing_reasoning)
                    processing_percentile_placeholder.empty()
                    st.session_state.processing_percentile = round(get_modified_percentile(id, df, cluster_assignment, clustering_model, index, st.session_state.processing_rating, "processing_level"),2)
                    processing_percentile_placeholder.write(f"This business is at the {st.session_state.processing_percentile}th percentile of similar businesses")
                    st.session_state.overall_score = ind_score_overall(df, id, processing_rating=st.session_state.processing_rating)['overall with strategy']
                    print(st.session_state.overall_score)
                    overall_score_placeholder.subheader(f"Overall Solution Score: {st.session_state.overall_score}/10")


     ### ACCESS LEVEL SECTION ###
                    
     st.subheader("Access Level")
     st.write(f"How hard is it to retrieve the relevant materials for this {business['product']}?")
     if not st.session_state.access_rating:
          st.session_state.access_rating = round(business['access_level'],2)
     access_rating_placeholder = st.empty()
     access_rating_placeholder.write(st.session_state.access_rating)

     if not st.session_state.access_percentile:
          st.session_state.access_percentile = round(percentiles['business_access_percentile'],2)
     access_percentile_placeholder = st.empty()
     access_percentile_placeholder.write(f"This business is at the {st.session_state.access_percentile}th percentile of similar businesses")
     
     with st.expander("See reasoning"):
          if not st.session_state.access_reasoning:
               st.session_state.access_reasoning = business['access_level_reasoning']
          access_reasoning_placeholder = st.empty()
          access_reasoning_placeholder.write(st.session_state.access_reasoning)

     with st.expander("I would like to modify this section"):
          with st.form("Edit Access Level"):
               st.write("Please enter your desired content. Leave an item blank if you'd like to keep the original content.")
               access_input = st.number_input("Enter new rating", placeholder="Enter")
               if processing_input <= 1 and processing_input >= 0:
                    st.session_state.access_rating = access_input
                    add_to_edited(id, 'access_level', access_input)
               else:
                    st.write("Sorry! The input must be between 0 and 1")
               access_reasoning_input = st.text_input("Enter new reasoning", placeholder = "Enter")
               if access_reasoning_input != "":
                    st.session_state.access_reasoning = access_reasoning_input
               submitted = st.form_submit_button("Submit")
               if submitted:
                    access_rating_placeholder.empty()
                    access_rating_placeholder.write(round(st.session_state.access_rating,2))
                    access_reasoning_placeholder.empty()
                    access_reasoning_placeholder.write(st.session_state.access_reasoning)
                    access_percentile_placeholder.empty()
                    st.session_state.access_percentile = round(get_modified_percentile(id, df, cluster_assignment, clustering_model, index, st.session_state.access_rating, "access_level"),2)
                    access_percentile_placeholder.write(f"This business is at the {st.session_state.access_percentile}th percentile of similar businesses")
                    st.session_state.overall_score = ind_score_overall(df, id, access_rating=st.session_state.access_rating)['overall with strategy']


     ### EMBEDDED VALUE SECTION ###

     st.subheader("Embedded Value Rating")
     st.write(f"How much value do the relevant materials contain for {business['product']}?")
     if not st.session_state.embedded_value_rating:
          st.session_state.embedded_value_rating = round(business['embedded_value'],2)
     embedded_value_rating_placeholder = st.empty()
     embedded_value_rating_placeholder.write(st.session_state.embedded_value_rating)

     if not st.session_state.embedded_value_percentile:
          st.session_state.embedded_value_percentile = round(percentiles['business_embedded_percentile'],2)
     embedded_value_percentile_placeholder = st.empty()
     embedded_value_percentile_placeholder.write(f"This business is at the {st.session_state.embedded_value_percentile}th percentile of similar businesses")

     with st.expander("See reasoning"):
          if not st.session_state.embedded_value_reasoning:
               st.session_state.embedded_value_reasoning = business['embedded_value_reasoning']
          embedded_value_reasoning_placeholder = st.empty()
          embedded_value_reasoning_placeholder.write(st.session_state.embedded_value_reasoning)
     with st.expander("I would like to modify this section"):
          with st.form("Edit Embedded Value"):
               st.write("Please enter your desired content. Leave an item blank if you'd like to keep the original content.")
               embedded_value_input = st.number_input("Enter new rating", placeholder="Enter")
               if embedded_value_input <= 1 and embedded_value_input >=0:
                    st.session_state.embedded_value_rating = embedded_value_input
                    add_to_edited(id, 'embedded_value', embedded_value_input)
               else:
                    st.write("Sorry! The input must be between 0 and 1")
               embedded_value_reasoning_input = st.text_input("Enter new reasoning", placeholder = "Enter")
               if embedded_value_reasoning_input != "":
                    st.session_state.embedded_value_reasoning = embedded_value_reasoning_input
               # Every form must have a submit button.
               submitted = st.form_submit_button("Submit")
               if submitted:
                    embedded_value_rating_placeholder.empty()
                    embedded_value_rating_placeholder.write(round(st.session_state.embedded_value_rating,2))
                    embedded_value_reasoning_placeholder.empty()
                    embedded_value_reasoning_placeholder.write(st.session_state.embedded_value_reasoning)
                    embedded_value_percentile_placeholder.empty()
                    st.session_state.embedded_value_percentile = round(get_modified_percentile(id, df, cluster_assignment, clustering_model, index, st.session_state.embedded_value_rating, "embedded_value"),2)
                    embedded_value_percentile_placeholder.write(f"This business is at the {st.session_state.embedded_value_percentile}th percentile of similar businesses")
                    st.session_state.overall_score = ind_score_overall(df, id, embedded_value_rating=st.session_state.embedded_value_rating)['overall with strategy']


     ### BUSINESS STRATEGY SECTION ###
                    
     st.subheader("Business Strategies Deployed:")
     for i, c in enumerate(business['categories']):
          with st.expander(strat_full_names[c]):
               st.write(strat_descriptions[c])
               st.write("Reasoning:")
               st.write(business['categories_reasonings'][i] if (len(business['categories_reasonings']) == len(business['categories'])) else "No reasoning provided")
     st.subheader(f"How does the {business['product']} business compare with similar businesses in the Circular Economy? - The Circular Matrix")
     similar_businesses = df[df['id'].isin(clusters[cluster_assignment[id]])]
     st.write(plot_matrix(similar_businesses, business['processing_level'], business['access_level']))
     st.header("Recommended Business Strategy")
     suggested = get_suggestion(st.session_state.processing_rating, business['access_level'], business['embedded_value'])
     for c in suggested:
          if c in business['categories']:
               with st.expander(f"{c}: Already deployed!"):
                    st.write(strat_descriptions[c])
          else:
               with st.expander(f"{c}: Not yet deployed"):
                    st.write(strat_descriptions[c])


if __name__ == "__main__":
     report(1)