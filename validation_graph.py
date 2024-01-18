import json
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import mplcursors
from scipy.stats import linregress
import numpy as np

# Your data
data = {
    1: 9.3, 2: 8.5, 3: 8.7, 4: 9.2, 5: 9.3, 6: 7.0, 7: 7.2, 8: 4.3, 9: 4.7, 10: 7.2,
    11: 7.3, 12: 3.3, 13: 9.3, 14: 5.2, 15: 6.5, 16: 9.8, 17: 9.7, 18: 6.7, 19: 10,
    20: 10, 21: 10.0, 22: 7.0, 23: 9.0, 24: 9.2, 25: 9.8, 26: 10, 27: 6.8, 28: 4.3,
    29: 7.7, 30: 7.2, 31: 10, 32: 4.7, 33: 9.5, 34: 4.0, 35: 6.2, 36: 10, 37: 10,
    38: 10, 39: 9.3, 40: 7.2, 41: 9.0, 42: 7.5, 43: 9.2, 44: 6.7, 45: 7.7, 46: 7.7,
    47: 8.2, 48: 7.7, 49: 7.7, 50: 7.7, 51: 6.7, 52: 10, 53: 7.7, 54: 10, 55: 9.2,
    56: 2.7, 57: 9.2, 58: 4.3, 59: 7.7, 60: 10, 61: 10, 62: 10, 63: 6.7, 64: 4.0,
    65: 7.7, 66: 6.7, 67: 4.7, 68: 4.2, 69: 5.7, 70: 8.8, 71: 10, 72: 10, 73: 4.3,
    74: 4.0, 75: 6.2, 76: 4.3, 77: 2.5, 78: 6.7, 79: 6.3, 80: 4.2, 81: 8.7, 82: 9.5,
    83: 7.3, 84: 7.7, 85: 6.2, 86: 10, 87: 10, 88: 9.0, 89: 10, 90: 7.7, 91: 7.7,
    92: 8.7, 93: 8.3, 94: 10, 95: 4.0, 96: 10, 97: 7.3, 98: 10.0, 99: 8.8, 100: 4.2,
    101: 10, 102: 7.8, 103: 9.2, 104: 5.5, 105: 10, 106: 10, 107: 10, 108: 8.7,
    109: 4.5, 110: 10, 111: 4.5, 112: 7.7, 113: 9.7, 114: 10, 115: 8.2,
    116: 4.3, 117: 10, 118: 9.2, 119: 9.5, 120: 9.8, 121: 10, 122: 10, 123: 10,
    124: 7.7, 125: 7.7, 126: 9.0, 127: 10.0, 128: 9.2, 129: 6.8, 130: 9.3,
    131: 10, 132: 10, 133: 10, 134: 8.7
}
df2 = pd.read_json('outputs/extracted_data_validation_dataset.jsonl', lines=True)
df = pd.DataFrame(list(data.items()), columns=['id', 'ratings'])

merged_df = pd.merge(df, df2, on='id')

merged_df = merged_df[(merged_df['ratings'] != 10) | (merged_df['circular_economy'] != 0)]

# Filter out outliers where total_raised is above 200

# Linear regression
slope, intercept, r_value, p_value, std_err = linregress(merged_df['ratings'], merged_df['circular_economy'])
line = slope * merged_df['ratings'] + intercept

# Higher-order polynomial regression (e.g., order=2)
poly_order = 2
coefficients = np.polyfit(merged_df['ratings'], merged_df['circular_economy'], poly_order)
poly_line = np.polyval(coefficients, merged_df['ratings'])

# Streamlit App
st.title('Overall Ratings and Circular Economy Correlation')

selected_metric = st.selectbox('Select a metric:', ['ratings'])

fig, ax = plt.subplots(figsize=(12, 8))
sns.regplot(x='ratings', y='circular_economy', data=merged_df, ax=ax, scatter_kws={'s': 50, 'alpha': 0.7}, order=poly_order)

# Cursor for hover
cursor = mplcursors.cursor(ax, hover=True)
cursor.connect("add", lambda sel: sel.annotation.set_text(f"ID: {int(merged_df['id'].iloc[sel.target.index])}"))

ax.set_xlabel(selected_metric.capitalize())
ax.set_ylabel('Circular Economy')
ax.set_title(f'Correlation: {selected_metric.capitalize()} vs Circular Economy Score')

# Display the chart using Streamlit
st.pyplot(fig)