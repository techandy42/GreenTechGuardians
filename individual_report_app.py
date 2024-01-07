import streamlit as st
import pandas as pd
from circular_matrix import plot_matrix, get_suggestion
from clustering_test import cluster_assignment, clusters
df = pd.read_json('outputs/combined_data_first_200_rows.jsonl', lines=True)
print(df)
strat_descriptions = {"RPO":"(retain product ownership) Producer rents or leases rather than selling",
                      "DFR":"(design for recycling)",
                      "PLE": "(product life extension)",
                      "PARTNERSHIP": "Partnering with specific technological expertise or institutional organization"
                      }
def report(id):
     business = df[df['id']==id].loc[0]
     st.title(business['product'])
     st.header("Problem Statement")
     st.write(business['problem'])
     # print(business.loc[0]['product'])
     st.header("Solution")
     st.write(business['summary'])
     with st.expander("More"):
          st.write(business['solution'])
     st.write("Processing level:")
     st.write(round(business['processing_level'],2))
     st.write("Access level:")
     st.write(round(business['access_level'],2))
     st.write("Embedded value rating:")
     st.write(round(business['embedded_value'],2))
     st.write("Business Strategies:")
     for c in business['categories']:
          with st.expander(c):
               st.write(strat_descriptions[c])
     similar_businesses = df[df['id'].isin(clusters[cluster_assignment[id]])]
     st.write(plot_matrix(similar_businesses, business['processing_level'], business['access_level']))
     st.header("Recommended Business Strategy")
     for c in get_suggestion(business['processing_level'], business['access_level'], business['embedded_value']):
          with st.expander(c):
               st.write(strat_descriptions[c])
report(1)