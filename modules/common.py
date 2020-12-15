import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


@st.cache # efforless app performance tuning 
def load_data(data):
	df = pd.read_csv(data,index_col='Date',parse_dates=True) #parse date values as datetimeindex
	df = df.apply(pd.to_numeric) #stock prices are numeric fields
	return df

# Function to normalize the prices based on the initial price
# The function simply divides every stock by it's price at the start date (i.e.: Date = 2012-01-12)	
def normalize(df):
  x = df.copy()

  # Loop through each stock (while ignoring time columns with index 0)
  for i in x.columns:
    x[i] = x[i]/x[i][0]
  return x

def interactive_plot(df, plot_title='',xaxes_title='',yaxes_title='',yaxes_prefix=''):
  fig = px.line(title = plot_title,width=860, height=450)

  # Loop through each stock (x is the datetime index)
  for i in df.columns:
    fig.add_scatter(x = df.index, y = df[i], name = i) # add a new scatter trace

  fig.update_xaxes(dtick="M12",title_text=xaxes_title)
  fig.update_yaxes(title_text=yaxes_title,tickprefix=yaxes_prefix)

  st.plotly_chart(fig)


# Let's define a function to calculate stocks daily returns (for all stocks) 
def daily_return(df):
  df_daily_return = df.copy()

  # Loop through each stock
  for i in df.columns:
    
    # Loop through each row belonging to the stock
    for j in range(1, len(df)):

      # Calculate the percentage of change from the previous day
      df_daily_return[i][j] = ((df[i][j]- df[i][j-1])/df[i][j-1]) * 100
    
    # set the value of first row to zero since the previous value is not available
    df_daily_return[i][0] = 0
  
  return df_daily_return
  