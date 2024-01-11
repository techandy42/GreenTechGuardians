import pandas as pd
import numpy as np

import os
from dotenv import load_dotenv
import pinecone
load_dotenv()
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')
index_name = 'greentechguardians'
index = pinecone.Index(index_name)

import pandas as pd
df = pd.read_json('outputs/combined_data_first_200_rows.jsonl', lines=True)
vector_ids = [str(id) for id in df["id"].tolist()]
# Fetch embeddings
fetch_results = index.fetch(ids=vector_ids)
fetch_results = fetch_results.to_dict()['vectors']
embeddings = [fetch_results[str(id)]['values'] for id in df["id"].tolist()]

from sklearn.cluster import KMeans

# solutions = list(df['solution'])
embedded_values = list(df['embedded_value'])
access_levels = list(df['access_level'])
processing_levels = list(df['processing_level'])

# # # Normalize the embeddings to unit length
embeddings = embeddings /  np.linalg.norm(embeddings, axis=1, keepdims=True)
clustering_model = KMeans(n_clusters=10)
clustering_model.fit(embeddings)
cluster_assignment = clustering_model.labels_
print(cluster_assignment)

# clustered_sentences = {}
# for sentence_id, cluster_id in enumerate(cluster_assignment):
#     if cluster_id not in clustered_sentences:
#         clustered_sentences[cluster_id] = []
#     clustered_sentences[cluster_id].append(sentence_id)

clusters = {}
for i in range(len(cluster_assignment)):
    if cluster_assignment[i] in clusters:
        clusters[cluster_assignment[i]].append(i+1)
    else:
        clusters[cluster_assignment[i]] = [i+1]
print(clusters)

cluster_stats = {}
for c in clusters:
    cluster_stats[c] = {}
    embedded_sum = 0
    access_sum = 0
    processing_sum = 0
    for id in clusters[c]:
        embedded_sum += embedded_values[id-1]
        access_sum += access_levels[id-1]
        processing_sum += processing_levels[id-1]
    cluster_stats[c]["embedded_values"] = [embedded_sum/len(clusters[c])]
    cluster_stats[c]["access_levels"] = [access_sum/len(clusters[c])]
    cluster_stats[c]["processing_levels"] = [processing_sum/len(clusters[c])]

print("cluster stats: ")
print(cluster_stats)
print("total stats:")
print("embedded values mean:")
print(sum(embedded_values)/len(embedded_values))
print("access level mean:")
print(sum(access_levels)/len(access_levels))
print("processing level mean:")
print(sum(processing_levels)/len(processing_levels))
    

