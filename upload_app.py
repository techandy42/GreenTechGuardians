import streamlit as st
import pandas as pd


file = st.file_uploader("Upload my own dataset")
if file is not None:
     df = pd.read_csv(file, encoding="latin-1")
     st.write(df)
