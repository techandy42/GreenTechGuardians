import streamlit as st
import pandas as pd
st.write("Original Data")
df = pd.read_csv('AI_EarthHack_Dataset.csv', encoding='latin-1')
st.write(df)

st.write("Extracted data row 0 - 50")
jsonObj = pd.read_json(path_or_buf='./outputs/extracted_data_row_0_to_50.jsonl', lines=True)
jsonObj

# for data visualization later
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import plotly
import plotly.graph_objs as go
import mpl_toolkits.mplot3d  
import matplotlib.cm as cm


