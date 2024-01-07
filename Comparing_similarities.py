from clustering_test import clustering_model
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from dotenv import load_dotenv
import pinecone
import os

load_dotenv()
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')
index_name = 'green'
index = pinecone.Index(index_name)

df = pd.read_json('outputs/combined_data_first_200_rows.jsonl', lines=True)

# Get business IDs and cluster assignments
vector_ids = [str(id) for id in df["id"].tolist()]
cluster_assignment = clustering_model.labels_ 

fetch_results = index.fetch(ids=vector_ids)
fetch_results = fetch_results.to_dict()['vectors']
embeddings = [fetch_results[str(id)]['values'] for id in df["id"].tolist()]

# Calculate percentiles within each cluster
percentile_results = {}

for cluster_id in np.unique(cluster_assignment):
    cluster_mask = (cluster_assignment == cluster_id)
    
    cluster_business_ids = df.loc[cluster_mask, "id"].tolist()
    cluster_embedded_values = df.loc[cluster_mask, "embedded_value"].tolist()
    cluster_access_levels = df.loc[cluster_mask, "access_level"].tolist()
    cluster_processing_levels = df.loc[cluster_mask, "processing_level"].tolist()
    
    cluster_embedded_percentiles = np.percentile(cluster_embedded_values, [25, 50, 75])
    cluster_access_percentiles = np.percentile(cluster_access_levels, [25, 50, 75])
    cluster_processing_percentiles = np.percentile(cluster_processing_levels, [25, 50, 75])
    
    # Store results in a dictionary
    percentile_results[cluster_id] = {
        "embedded_percentiles": cluster_embedded_percentiles,
        "access_percentiles": cluster_access_percentiles,
        "processing_percentiles": cluster_processing_percentiles,
        "business_ids": cluster_business_ids
    }

# Display
print(percentile_results)