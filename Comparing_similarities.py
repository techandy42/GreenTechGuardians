import pandas as pd
import openai
import numpy as np
from sklearn.cluster import KMeans

api_key = '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'
openai.api_key = api_key

target_embedded_mean = 0.5835858585858591
target_access_mean = 0.2772727272727276
target_processing_mean = 0.42752525252525264

df = pd.read_csv('./outputs/combined_data_first_200_rows.csv', encoding='latin-1')
solutions = list(df['solution'])
embedded_values = list(df['embedded_value'])
access_levels = list(df['access_level'])
processing_levels = list(df['processing_level'])

cluster_stats = {}

response = openai.Embedding.create(
    input=solutions[:200],  
    model="text-similarity-babbage-001"
)
solutions_embeddings = [d['embedding'] for d in response['data']]
solutions_embeddings = solutions_embeddings / np.linalg.norm(solutions_embeddings, axis=1, keepdims=True)


clustering_model = KMeans(n_clusters=8)
clustering_model.fit(solutions_embeddings)
cluster_assignment = clustering_model.labels_

for c in range(clustering_model.n_clusters):
    cluster_mask = (cluster_assignment == c)
    cluster_stats[c] = {
        "embedded_values": np.mean(np.array(embedded_values)[cluster_mask]),
        "access_levels": np.mean(np.array(access_levels)[cluster_mask]),
        "processing_levels": np.mean(np.array(processing_levels)[cluster_mask]),
    }

target_business_cluster = clustering_model.predict([[target_embedded_mean, target_access_mean, target_processing_mean]])[0]

target_cluster_stats = cluster_stats[target_business_cluster]

target_embedded_percentile = np.percentile(np.array(embedded_values), [25, 50, 75])
target_access_percentile = np.percentile(np.array(access_levels), [25, 50, 75])
target_processing_percentile = np.percentile(np.array(processing_levels), [25, 50, 75])

print("Embedded Value Percentiles:", target_embedded_percentile)
print("Access Level Percentiles:", target_access_percentile)
print("Processing Level Percentiles:", target_processing_percentile)