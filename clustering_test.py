import pandas as pd
import openai, numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity

api_key = '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'
openai.api_key = api_key

# resp = openai.Embedding.create(
#     input=["eating food", "I am hungry", "I am traveling" , "exploring new places"],
#     engine="text-similarity-davinci-001")
# resp['data'][0].keys()

# source: https://stackoverflow.com/questions/55619176/how-to-cluster-similar-sentences-using-bert
from sklearn.cluster import KMeans

df = pd.read_csv('./outputs/combined_data_first_200_rows.csv', encoding='latin-1')
solutions = list(df['solution'])
embedded_values = list(df['embedded_value'])
access_levels = list(df['access_level'])
processing_levels = list(df['processing_level'])
print(solutions[0])


# # Corpus with example sentences
# corpus = ['A man is eating food.',
#           'A man is eating a piece of bread.',
#           'Horse is eating grass.',
#           'A man is eating pasta.',
#           'A Woman is eating Biryani.',
#           'The girl is carrying a baby.',
#           'The baby is carried by the woman',
#           'A man is riding a horse.',
#           'A man is riding a white horse on an enclosed ground.',
#           'A monkey is playing drums.',
#           'Someone in a gorilla costume is playing a set of drums.',
#           'A cheetah is running behind its prey.',
#           'A cheetah chases prey on across a field.',
#           'The cheetah is chasing a man who is riding the horse.',
#           'man and women with their baby are watching cheetah in zoo'
#           ]
response = openai.Embedding.create(
    input=solutions[:800],
    model="text-similarity-babbage-001"
)
print(type(response['data']))

solutions_embeddings = [ d['embedding'] for d in response['data']]
# # Normalize the embeddings to unit length
solutions_embeddings = solutions_embeddings /  np.linalg.norm(solutions_embeddings, axis=1, keepdims=True)
clustering_model = KMeans(n_clusters=8)
clustering_model.fit(solutions_embeddings)
cluster_assignment = clustering_model.labels_
print(cluster_assignment)

clustered_sentences = {}
for sentence_id, cluster_id in enumerate(cluster_assignment):
    if cluster_id not in clustered_sentences:
        clustered_sentences[cluster_id] = []
    clustered_sentences[cluster_id].append(solutions[sentence_id])
print(clustered_sentences[1][:3])

clusters = {}
for i in range(len(cluster_assignment)):
    if cluster_assignment[i] in clusters:
        clusters[cluster_assignment[i]].append(i+1)
    else:
        clusters[cluster_assignment[i]] = [i+1]

cluster_stats = {}
for c in clusters:
    cluster_stats[c] = {}
    cluster_stats[c]["embedded_values"] = [sum(embedded_values)/len(embedded_values),]
    cluster_stats[c]["access_levels"] = [sum(access_levels)/len(access_levels),]
    cluster_stats[c]["processing_levels"] = [sum(processing_levels)/len(processing_levels),]
    

