import numpy as np
import plotly.express as px
import pandas as pd

def plot_avg(data,groupcol,aggcol,min = 0,max = None,width = 800,height = 400,title = 'title'):
    if max == None:
       max =  np.unique(data[groupcol]).shape[0] -1

    df_avg = data[[groupcol,aggcol]].groupby(groupcol).mean().sort_values(by = aggcol).reset_index()[min:max]


    fig = px.bar(df_avg,x = aggcol,y = groupcol,orientation='h',width = width,height=height,title=title)
   #  fig.update_layout(yaxis = dict(tickmode = 'linear'))
    return fig


def plot_counts(data,col,min = 0,max = None,width = 800,height = 400,title = 'title',barmode = None):
   if max == None:
      if type(col) == str:
         max =  np.unique(data[col]).shape[0]
      if type(col) == list:
         max =  np.unique(data[col[0]]).shape[0]

   if type(col) == str:
      df_counts = pd.DataFrame(data[col].value_counts()).reset_index().rename(columns = {col:f'{col}_counts','index':col}).sort_values(by = f'{col}_counts')
      fig = px.bar(df_counts,x = f'{col}_counts',y=col,orientation='h',width = width,height=height,title=title)
      fig.update_layout(yaxis = dict(tickmode = 'linear'))
   if type(col) == list:
      df_counts = pd.DataFrame(data[col].value_counts()).reset_index().rename(columns = {0:'counts'}).sort_values(by = 'counts')
      fig = px.bar(df_counts,x ='counts',y=col[0],color = col[1], barmode = barmode,orientation='h',width = width,height=height,title=title)


   return fig


def plot_scatter(data,col1,col2,col3 = None,x_limit = None,y_limit=None,names = None,width = 800,height = 400,title = 'title',
col1_name = None,col2_name = None,col3_name = None):
    df_scatter = data[[col1,col2,col3]]
    if x_limit != None:
        df_scatter = df_scatter[df_scatter[col1]<=x_limit]
    if y_limit != None:
        df_scatter = df_scatter[df_scatter[col2]<=y_limit]
    if names != None:
        df_scatter = df_scatter[df_scatter[col3].isin(names)]
    
    if col1_name == None:
        col1_name = col1
    if col2_name == None:
        col2_name = col2
    if col3_name == None:
        col3_name = col3

    fig = px.scatter(df_scatter,col1,col2,color = col3,width=width,height = height,title = title,
    labels={col1:col1_name, col2:col2_name, col3:col3_name})
    return fig