from clustering_test_validation import clustering_model
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from dotenv import load_dotenv
import pinecone
import os
from scipy.stats import percentileofscore
from openai import OpenAI

load_dotenv()
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')
index_name = 'greentechguardians'
index = pinecone.Index(index_name)
client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY']
)
df = pd.read_json('outputs/extracted_data_validation_dataset.jsonl', lines=True)

def get_embeddings(texts):
    response = client.embeddings.create(input=texts, model="text-embedding-ada-002")
    return [embedding.embedding for embedding in response.data]

vector_ids = [str(id) for id in df["id"].tolist()]
cluster_assignment = clustering_model.labels_

fetch_results = index.fetch(ids=vector_ids)
fetch_results = fetch_results.to_dict()['vectors']

embeddings = [fetch_results[str(id)]['values'] for id in df["id"].tolist()]
new_df = pd.read_json('outputs/extracted_data_validation_dataset.jsonl', lines=True)
new_vector_ids = [str(id) for id in new_df["id"].tolist()]

uploaded_df = pd.DataFrame(new_df)
uploaded_df['combined_text'] = uploaded_df.apply(lambda x: f"{x['product']} {x['summary']} {' '.join(x['categories'])}", axis=1)
new_index_name = 'greentechguardiansplus'
EMBEDDING_DIMENSION = 1536
new_index = pinecone.Index(new_index_name)
new_embedding = get_embeddings(uploaded_df['combined_text'].tolist())
print("=" * 10 + " OpenAI Embeddings Created " + "=" * 10)
to_upload = [(str(id), embedding) for id, embedding in zip(uploaded_df['id'], embeddings)]
new_index.upsert(vectors=to_upload)
user_uploaded = True


def get_percentile(business_id, df, cluster_assignment, clustering_model, index):
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

# # Example usage:
# business_id_to_check = 22  
# similar_businesses_info = get_percentile(business_id_to_check, df, cluster_assignment, clustering_model, index)
# print("Similar Businesses in Percentile:", similar_businesses_info["similar_businesses"])

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




