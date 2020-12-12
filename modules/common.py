import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Define a function to plot the entire dataframe
# The function takes in a dataframe df as an input argument and does not return anything back!
# The function performs data visualization
# Pandas works great with matplotlib, you can simply plot data directly from a Pandas DataFrame using plot() method
def show_plot(df, fig_title):
  fig = plt.figure(figsize=(20,10))
  sns.lineplot(data=df,x='Date',y='AAPL')
  st.pyplot(fig)


def interactive_plot(df, title):
  fig = px.line(title = title,width=900, height=550)

  # Loop through each stock (x is the datetime index)
  for i in df.columns:
    fig.add_scatter(x = df.index, y = df[i], name = i) # add a new scatter trace

  fig.update_xaxes(
    dtick="M12")

  st.plotly_chart(fig)

# Function to normalize the prices based on the initial price
# The function simply divides every stock by it's price at the start date (i.e.: Date = 2012-01-12)	
def normalize(df):
  x = df.copy()

  # Loop through each stock (while ignoring time columns with index 0)
  for i in x.columns:
    x[i] = x[i]/x[i][0]
  return x

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
  