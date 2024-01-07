import streamlit as st
import pandas as pd
from circular_matrix import plot_matrix
from clustering_test import cluster_assignment, clusters
df = pd.read_json('outputs/combined_data_first_200_rows.jsonl', lines=True)
print(df)
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
     st.write("processing level:")
     st.write(round(business['processing_level'],2))
     st.write("access level:")
     st.write(round(business['access_level'],2))
     st.write("embedded value rating:")
     st.write(round(business['embedded_value'],2))
     st.write("strategies:")
     st.write(business['categories'])
     st.write(plot_matrix(df, business['processing_level'], business['access_level']))
     # clusters[cluster_assignment[id]]
     # st.write(clusters[cluster_assignment[id]])
report(1)