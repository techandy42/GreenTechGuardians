from clustering_test import clustering_model
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from dotenv import load_dotenv
import pinecone
import os
from scipy.stats import percentileofscore

load_dotenv()
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')
index_name = 'greentechguardians'
index = pinecone.Index(index_name)

df = pd.read_json('outputs/extracted_data_training_dataset.jsonl', lines=True)

# Get business IDs and cluster assignments
vector_ids = [str(id) for id in df["id"].tolist()]
cluster_assignment = clustering_model.labels_

fetch_results = index.fetch(ids=vector_ids)
fetch_results = fetch_results.to_dict()['vectors']
embeddings = [fetch_results[str(id)]['values'] for id in df["id"].tolist()]

# percentile_results = {}

# for cluster_id in np.unique(cluster_assignment):
#     cluster_mask = (cluster_assignment == cluster_id)
    
#     cluster_business_ids = df.loc[cluster_mask, "id"].tolist()
#     cluster_embedded_values = df.loc[cluster_mask, "embedded_value"].tolist()
#     cluster_access_levels = df.loc[cluster_mask, "access_level"].tolist()
#     cluster_processing_levels = df.loc[cluster_mask, "processing_level"].tolist()
    
#     cluster_embedded_percentiles = np.percentile(cluster_embedded_values, [25, 50, 75])
#     cluster_access_percentiles = np.percentile(cluster_access_levels, [25, 50, 75])
#     cluster_processing_percentiles = np.percentile(cluster_processing_levels, [25, 50, 75])
    
#     # Store results in a dictionary
#     percentile_results[cluster_id] = {
#         "embedded_percentiles": cluster_embedded_percentiles,
#         "access_percentiles": cluster_access_percentiles,
#         "processing_percentiles": cluster_processing_percentiles,
#         "business_ids": cluster_business_ids
#     }


def get_similar_businesses_in_percentile(business_id, df, cluster_assignment, clustering_model, index):
    # Fetch the embedding for the given business ID
    fetch_result = index.fetch(ids=[str(business_id)])
    business_embedding = fetch_result.to_dict()['vectors'][str(business_id)]['values']

    # Get the cluster assignment for the business
    business_cluster = clustering_model.predict([business_embedding])[0]

    # Get the data for the specific cluster
    cluster_mask = (cluster_assignment == business_cluster)
    cluster_percentiles = {
        "embedded": np.percentile(df.loc[cluster_mask, "embedded_value"], np.mean(df.loc[df['id'] == business_id, "embedded_value"])),
        "access": np.percentile(df.loc[cluster_mask, "access_level"], np.mean(df.loc[df['id'] == business_id, "access_level"])),
        "processing": np.percentile(df.loc[cluster_mask, "processing_level"], np.mean(df.loc[df['id'] == business_id, "processing_level"]))
    }

    # Find business IDs within the same percentile
    similar_businesses = df.loc[cluster_mask, "id"].tolist()

    return {
        "business_cluster": business_cluster,
        "cluster_percentiles": cluster_percentiles,
        "similar_businesses": similar_businesses
    }

# Example usage:
business_id_to_check = 22  
similar_businesses_info = get_similar_businesses_in_percentile(business_id_to_check, df, cluster_assignment, clustering_model, index)
print("Similar Businesses in Percentile:", similar_businesses_info["similar_businesses"])

def get_percentiles_for_business(business_id, df, cluster_assignment, clustering_model, index):
    # Fetch the embedding for the given business ID
    fetch_result = index.fetch(ids=[str(business_id)])
    business_embedding = fetch_result.to_dict()['vectors'][str(business_id)]['values']

    business_cluster = clustering_model.predict([business_embedding])[0]

    cluster_mask = (cluster_assignment == business_cluster)
    cluster_embedded_values = df.loc[cluster_mask, "embedded_value"].tolist()
    cluster_access_levels = df.loc[cluster_mask, "access_level"].tolist()
    cluster_processing_levels = df.loc[cluster_mask, "processing_level"].tolist()

    business_embedded_percentile = percentileofscore(cluster_embedded_values, df.loc[df['id'] == business_id, "embedded_value"].iloc[0])
    business_access_percentile = percentileofscore(cluster_access_levels, df.loc[df['id'] == business_id, "access_level"].iloc[0])
    business_processing_percentile = percentileofscore(cluster_processing_levels, df.loc[df['id'] == business_id, "processing_level"].iloc[0])

    return {
        "business_embedded_percentile": business_embedded_percentile,
        "business_access_percentile": business_access_percentile,
        "business_processing_percentile": business_processing_percentile
    }

# Example usage:
business_id_to_check = 22 
percentile_results = get_percentiles_for_business(business_id_to_check, df, cluster_assignment, clustering_model, index)
print("Exact Percentiles for Business within its Cluster:")
print("Business Embedded Value Percentile:", percentile_results["business_embedded_percentile"])
print("Business Access Level Percentile:", percentile_results["business_access_percentile"])
print("Business Processing Level Percentile:", percentile_results["business_processing_percentile"])
