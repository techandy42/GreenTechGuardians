import pandas as pd

df = pd.read_csv('./outputs/combined_data_first_200_rows.csv', encoding='latin-1')
solutions = list(df['solution'])
embedded_values = list(df['embedded_value'])
access_levels = list(df['access_level'])
processing_levels = list(df['processing_level'])

# modifies score_tracker according to data, regular represents positive correlation
def scorer(score_tracker, data, regular):
    if regular:
        for idx in range(len(solutions)):
            var = data[idx]
            if var <= 0.3:
                score_tracker[idx+1] = 1
            elif var <= 0.6:
                score_tracker[idx+1] = 2
            elif var <= 0.9:
                score_tracker[idx+1] = 3
            elif var <= 1.2:
                score_tracker[idx+1] = 4
            elif var <= 1.5:
                score_tracker[idx+1] = 5
            elif var <= 1.8:
                score_tracker[idx+1] = 6
            elif var <= 2.1:
                score_tracker[idx+1] = 7
            elif var <= 2.4:
                score_tracker[idx+1] = 8
            elif var <= 2.7:
                score_tracker[idx+1] = 9
            elif var <= 3.0:
                score_tracker[idx+1] = 10
    else:
        for idx in range(len(solutions)):
            var = data[idx]
            if var <= 0.3:
                score_tracker[idx+1] = 10
            elif var <= 0.6:
                score_tracker[idx+1] = 9
            elif var <= 0.9:
                score_tracker[idx+1] = 8
            elif var <= 1.2:
                score_tracker[idx+1] = 7
            elif var <= 1.5:
                score_tracker[idx+1] = 6
            elif var <= 1.8:
                score_tracker[idx+1] = 5
            elif var <= 2.1:
                score_tracker[idx+1] = 4
            elif var <= 2.4:
                score_tracker[idx+1] = 3
            elif var <= 2.7:
                score_tracker[idx+1] = 2
            elif var <= 3.0:
                score_tracker[idx+1] = 1

# scores based on each factor
scores_em = {} # higher embedded value -> higher score
scores_ac = {} # higher access level -> lower score
scores_pr = {} # higher processing level -> lower score

scorer(scores_em, embedded_values, True)
scorer(scores_ac, access_levels, False)
scorer(scores_pr, processing_levels, False)

# make new dict with avg scores from each scores dict above
avg_scores = {}
for idx in range(len(solutions)):
    avg_scores[idx+1] = (scores_em[idx+1] + scores_ac[idx+1] + scores_pr[idx+1]) / 3

# gives an overall score based on the average of individual scores
scores_overall = {}
for idx in range(len(solutions)):
    var = avg_scores[idx+1]
    if var <= 0.3:
        scores_overall[idx+1] = 1
    elif var <= 0.6:
        scores_overall[idx+1] = 2
    elif var <= 0.9:
        scores_overall[idx+1] = 3
    elif var <= 1.2:
        scores_overall[idx+1] = 4
    elif var <= 1.5:
        scores_overall[idx+1] = 5
    elif var <= 1.8:
        scores_overall[idx+1] = 6
    elif var <= 2.1:
        scores_overall[idx+1] = 7
    elif var <= 2.4:
        scores_overall[idx+1] = 8
    elif var <= 2.7:
        scores_overall[idx+1] = 9
    elif var <= 3.0:
        scores_overall[idx+1] = 10


# Using percentiles to score: split by 10s 
# Every 10th percentile increments score by 1
