import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import plotly
import plotly.graph_objs as go
import mpl_toolkits.mplot3d  
import matplotlib.cm as cm

# def quadrant_chart(all_process_level, all_access_level, this_process_level, this_access_level):

#     # make the data easier to work with by putting it in a dataframe
#     data = pd.DataFrame({'x': all_process_level, 'y': all_access_level})

#     # let the user specify their own axes
#     fig = plt.figure(figsize=(8,8))

#     ax = plt.axes()

#     # calculate averages up front to avoid repeated calculations
#     y_avg = data['y'].mean()
#     x_avg = data['x'].mean()

#     # set x limits
#     adj_x = max((data['x'].max() - x_avg), (x_avg - data['x'].min())) * 1.1
#     lb_x, ub_x = (x_avg - adj_x, x_avg + adj_x)
#     ax.set_xlim(lb_x, ub_x)

#     # set y limits
#     adj_y = max((data['y'].max() - y_avg), (y_avg - data['y'].min())) * 1.1
#     lb_y, ub_y = (y_avg - adj_y, y_avg + adj_y)
#     ax.set_ylim(lb_y, ub_y)

#     # set x tick labels
# #     ax.set_xticks([(x_avg - adj_x / 2), (x_avg + adj_x / 2)])
# #     ax.set_xticklabels("process level")
    
# #     ax.set_yticks([(y_avg - adj_y / 2), (y_avg + adj_y / 2)])
# #     ax.set_yticklabels("access level", rotation='vertical', va='center')

#     # plot points and quadrant lines
#     ax.scatter(x=data['x'], y=data['y'], c='lightblue', edgecolor='darkblue',
#     zorder=99)
#     ax.axvline(x_avg, c='k', lw=1)
#     ax.axhline(y_avg, c='k', lw=1)
#     plt.plot(this_process_level, this_access_level, 'g*')
#     plt.title('Circular Matrix', fontsize=16)
#     plt.ylabel('Access Level', fontsize=14)
#     plt.xlabel('Process Level', fontsize=14)
#     return fig

# chart = quadrant_chart(
#     all_process_level=np.random.random(15),
#     all_access_level=np.random.random(15),
#     this_process_level=0.6,
#     this_access_level=0.2
# )
# st.write(chart)

# plt
# plt.show()

import plotly.express as px
# df = pd.DataFrame({'processing_level':[0.1, 0.2, 0.3, 0.5, 0.1, 0.9], 'access_level':[0.4, 0.5, 0.7, 0.1, 0.9, 0.3], 
#                    'categories': ['a','b','c','b','e','a']})
def plot_matrix(df, this_processing, this_access):
     fig = px.scatter(df,x = 'processing_level', y = 'access_level',hover_data=['categories'],  width=500, height=500)
     fig.add_scatter(x=[this_processing],
                    y=[this_access],
                    marker=dict(
                         color='red',
                         size=10
                    ),
                    name='this business')
     
     fig.add_hline(y=0.5, line_color = "grey")
     fig.add_vline(x=0.5, line_color = "grey")
     fig.update_layout(yaxis_range=[0,1])
     fig.update_layout(xaxis_range=[0,1])
     fig.update_traces(line_color='#ffffff', line_width=5)
     fig.update_xaxes(linewidth=1, linecolor='grey', mirror=True, ticks='inside', 
     showline=True)
     fig.update_yaxes(linewidth=1, linecolor='grey', mirror=True, ticks='inside', 
     showline=True)
     # fig.show()
     return fig
# st.write(plot_matrix(df, 0.2, 0.8))

def get_suggestion(processing_level, access_level, embedded_value):
     if processing_level > 0.5 and access_level > 0.5:
          if embedded_value > 0.5:
               return ["PLE"]
          else:
               return ["DFR", "RPO"]
     elif processing_level > 0.5 and access_level <= 0.5:
          if embedded_value > 0.5:
               return ["DFR"]
          else:
               return ["DFR", "PARTNERSHIP"]
     elif processing_level <= 0.5 and access_level > 0.5:
          if embedded_value > 0.5:
               return ["PLE", "RPO"]
          else:
               return ["DFR", "PARTNERSHIP"]
     else:
          if embedded_value > 0.5:
               return ["PLE", "DFR"]
          else:
               return ["DFR"]

     