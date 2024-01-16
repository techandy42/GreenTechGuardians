import pandas as pd
from comparing_similarities import get_percentiles_for_business
from clustering_test import clustering_model
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from dotenv import load_dotenv
import pinecone
import os
from scipy.stats import percentileofscore
from circular_matrix import get_suggestion

df = pd.read_json('outputs/extracted_data_training_dataset.jsonl', lines=True)
solutions = list(df['solution'])
ids = list(df['id'])
embedded_values = list(df['embedded_value'])
access_levels = list(df['access_level'])
processing_levels = list(df['processing_level'])

# functions to get scores for individual businesses
# embedded (regular), access (opposite), processing (opposite), average, overall, percentile
# gets all scores for an individual business
def ind_score_overall(df, business_id, processing_rating = None, access_rating = None, embedded_value_rating = None):
    ids = list(df['id'])
    embedded_values = list(df['embedded_value'])
    access_levels = list(df['access_level'])
    processing_levels = list(df['processing_level'])
    categories = list(df['categories'])
    score_tracker = {}
    var = embedded_values[business_id-1]
    if embedded_value_rating:
        var = embedded_value_rating
    score_tracker["embedded score"] = var * 10

    var = access_levels[business_id-1]
    if access_rating:
        var = access_rating
        print("entered var is: ")
        print(var)
    score_tracker["access score"] = 10 - (var * 10) + 1

    var = processing_levels[business_id-1]
    if processing_rating:
        var = processing_rating
    score_tracker["processing score"] = 10 - (var * 10) + 1

    score_tracker["average score"] = (score_tracker["embedded score"] + score_tracker["access score"] + score_tracker["processing score"]) / 3.0
    score_tracker["overall score"] = score_tracker["average score"]

    dict = get_percentiles_for_business(business_id, df, cluster_assignment, clustering_model, index)
    score_tracker["percentile score"] = min((dict["business_embedded_percentile"] // 10) + 1, 10)
    
    recommended = get_suggestion(processing_levels[business_id-1], access_levels[business_id-1], embedded_values[business_id-1])
    category = categories[business_id-1]
    if recommended == category:
        score_tracker["overall with strategy"] = min(((score_tracker["overall score"] + score_tracker["percentile score"] // 2) +1), 10)
    else:
        score_tracker["overall with strategy"] = min((score_tracker["overall score"] + score_tracker["percentile score"] // 2), 10)
    
    return score_tracker

# modifies score_tracker according to data, regular represents positive correlation
def scorer(data, df, regular):
    # data: list of specific data, ids: list of business ids
    ids = list(df['id'])
    score_tracker = {}
    if regular:
        for idx in range(len(ids)):
            var = data[idx]
            # if var <= 0.3:
            #     score_tracker[idx+1] = 1
            # elif var <= 0.6:
            #     score_tracker[idx+1] = 2
            # elif var <= 0.9:
            #     score_tracker[idx+1] = 3
            # elif var <= 1.2:
            #     score_tracker[idx+1] = 4
            # elif var <= 1.5:
            #     score_tracker[idx+1] = 5
            # elif var <= 1.8:
            #     score_tracker[idx+1] = 6
            # elif var <= 2.1:
            #     score_tracker[idx+1] = 7
            # elif var <= 2.4:
            #     score_tracker[idx+1] = 8
            # elif var <= 2.7:
            #     score_tracker[idx+1] = 9
            # elif var <= 3.0:
            #     score_tracker[idx+1] = 10
            score_tracker[idx+1] = var * 10
    else:
        for idx in range(len(ids)):
            var = data[idx]
            # if var <= 0.3:
            #     score_tracker[idx+1] = 10
            # elif var <= 0.6:
            #     score_tracker[idx+1] = 9
            # elif var <= 0.9:
            #     score_tracker[idx+1] = 8
            # elif var <= 1.2:
            #     score_tracker[idx+1] = 7
            # elif var <= 1.5:
            #     score_tracker[idx+1] = 6
            # elif var <= 1.8:
            #     score_tracker[idx+1] = 5
            # elif var <= 2.1:
            #     score_tracker[idx+1] = 4
            # elif var <= 2.4:
            #     score_tracker[idx+1] = 3
            # elif var <= 2.7:
            #     score_tracker[idx+1] = 2
            # elif var <= 3.0:
            #     score_tracker[idx+1] = 1
            score_tracker[idx+1] = 10 - (var * 10) + 1
    return score_tracker

# scores based on each factor
scores_em = scorer(embedded_values, df, True) # higher embedded value -> higher score
scores_ac = scorer(access_levels, df, False) # higher access level -> lower score
scores_pr = scorer(processing_levels, df, False) # higher processing level -> lower score

# scorer(scores_em, embedded_values, True)
# scorer(scores_ac, access_levels, False)
# scorer(scores_pr, processing_levels, False)

# make new dict with avg scores from each scores dict above
def average_scores(df):
    ids = list(df['id'])
    embedded_values = list(df['embedded_value'])
    access_levels = list(df['access_level'])
    processing_levels = list(df['processing_level'])
    avg_scores = {}
    for idx in range(len(ids)):
        avg_scores[idx+1] = round((embedded_values[idx] + access_levels[idx] + processing_levels[idx]) / 3.0, 2)
    return avg_scores

avg_scores = average_scores(df)

# gives an overall score based on the average of individual scores
def score_overall(avg_scores, df):
    ids = list(df['id'])
    scores_overall = {}
    for key in avg_scores:
        var = avg_scores[key]
        # if var <= 0.3:
        #     scores_overall[key] = 1
        # elif var <= 0.6:
        #     scores_overall[key] = 2
        # elif var <= 0.9:
        #     scores_overall[key] = 3
        # elif var <= 1.2:
        #     scores_overall[key] = 4
        # elif var <= 1.5:
        #     scores_overall[key] = 5
        # elif var <= 1.8:
        #     scores_overall[key] = 6
        # elif var <= 2.1:
        #     scores_overall[key] = 7
        # elif var <= 2.4:
        #     scores_overall[key] = 8
        # elif var <= 2.7:
        #     scores_overall[key] = 9
        # else:
        #     scores_overall[key] = 10
        scores_overall[key] = var * 10
    return scores_overall

scores_overall = score_overall(avg_scores, df)

# Using percentiles to score: split by 10s 
# Every 10th percentile increments score by 1
vector_ids = [str(id) for id in df["id"].tolist()]
cluster_assignment = clustering_model.labels_
load_dotenv()
pinecone.init(api_key=os.environ.get("PINECONE_API_KEY"), environment='us-west4-gcp-free')
index_name = 'greentechguardians'
index = pinecone.Index(index_name)

def percentile_scoring(df, cluster_assignment, clustering_model, index):
    ids = list(df['id'])
    percentile_score = {}
    for id in ids:
        dict = get_percentiles_for_business(id, df, cluster_assignment, clustering_model, index)
        percentile_score[id] = min((dict["business_embedded_percentile"] // 10) + 1, 10)
    return percentile_score

percentile_score = percentile_scoring(df, cluster_assignment, clustering_model, index)

# scores by comparing with recommended strategies
def strategy_scoring(df, scores_overall, percentile_score):
    categories = list(df['categories'])
    ids = list(df['id'])
    embedded_values = list(df['embedded_value'])
    access_levels = list(df['access_level'])
    processing_levels = list(df['processing_level'])
    strategy_score = {}
    for idx in range(len(ids)):
        recommended = get_suggestion(processing_levels[idx], access_levels[idx], embedded_values[idx])
        category = categories[idx]
        if recommended == category:
            strategy_score[idx+1] = min(((scores_overall[idx+1] + percentile_score[idx+1] // 2) +1), 10)
        else:
            strategy_score[idx+1] = min(((scores_overall[idx+1] + percentile_score[idx+1] // 2)), 10)
    return strategy_score

strategy_score = strategy_scoring(df, scores_overall, percentile_score)
print(ind_score_overall(df, 1, processing_rating=0.9))
print(ind_score_overall(df, 1, processing_rating=0.1))
print(ind_score_overall(df, 1, access_rating=0.1))