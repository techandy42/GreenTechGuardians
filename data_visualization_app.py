import streamlit as st
import pandas as pd

extracted = pd.read_json(path_or_buf='./outputs/combined_data_first_200_rows.jsonl', lines=True)
extracted = extracted.to_numpy()
ids = extracted[:,0]
embedded_values = extracted[:,3]
access = extracted[:,4]
process = extracted[:,5]
categories = extracted[:,6]

# for data visualization later
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import plotly
import plotly.graph_objs as go
import mpl_toolkits.mplot3d  
import matplotlib.cm as cm

x_data = embedded_values
y_data = process
z_data = access

def scatter_results_3d(x_data, y_data, z_data, keyword):
    trace1 = go.Scatter3d(
        x=x_data,
        y=y_data,
        z=z_data,
        mode='markers',
        marker=dict(size=4, color='blue', opacity=0.8)
    )
    axis = dict(
            showbackground=False, # show axis background
            backgroundcolor="rgb(204, 204, 204)", # set background color to grey
            gridcolor="rgb(255, 255, 255)",       # set grid line color
            zerolinecolor="rgb(255, 255, 255)",   # set zero grid line color
        )
    layout = go.Layout(
            title= f"Businesses related to {keyword}", # set plot title
            autosize=False,
            width=500, height=500,
            margin=dict(l=65, r=50, b=65, t=90),
            scene=go.Scene(  # axes are part of a 'scene' in 3d plots
                xaxis=go.XAxis(axis), # set x-axis style
                yaxis=go.YAxis(axis), # set y-axis style
                zaxis=go.ZAxis(axis)),  # set z-axis style
    )
    fig = go.Figure(data=go.Data([trace1]), layout=layout)
    fig.update_layout(scene = dict(
                        xaxis_title='embedded value rating',
                        yaxis_title='level of processing',
                        zaxis_title='level of access')

    )
    fig.update_layout(scene = dict(yaxis=dict(dtick=1, type='log')))
    st.plotly_chart(fig)

if __name__ == "__main__":
    scatter_results_3d(x_data, y_data, z_data, "first 200 rows")