import pandas as pd
import openai, numpy as np
from openai.embeddings_utils import get_embedding, cosine_similarity

api_key = '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'
openai.api_key = api_key

resp = openai.Embedding.create(
    input=["eating food", "I am hungry", "I am traveling" , "exploring new places"],
    engine="text-similarity-davinci-001")
