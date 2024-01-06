import streamlit as st
import pandas as pd
df = pd.read_csv('AI_EarthHack_Dataset.csv', encoding='latin-1')
st.write(df)
