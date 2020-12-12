import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from copy import copy
from scipy import stats
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from modules.common import show_plot,interactive_plot,normalize,daily_return

@st.cache
def load_data(data):
	df = pd.read_csv(data,index_col='Date',parse_dates=True) #parse date values as datetimeindex
	df = df.apply(pd.to_numeric) #stock prices are numeric fields
	return df

def run_stock_analysis():
	stock_df = load_data('data/stock.csv')

	submenu = st.sidebar.selectbox("SubMenu",["Descriptive statistics","Stock Daily Returns"])

	if submenu == "Descriptive statistics":

		with st.beta_expander("Raw stock prices data sorted by dates"):
			st.dataframe(stock_df)
		
		with st.beta_expander("Missing data check | no missing closing price found"):
			st.dataframe(stock_df.isnull().sum())

		st.subheader("Descriptive statistics of the stock prices")
		st.dataframe(stock_df.describe())
		st.write("""
		##### Observations:
		- ###### AMZN stock has the highest dispersion (standard deviation) from the mean dollar
		- ###### Also, amongst all AMZN has touched the highest closing price during the period
		- ###### All but IBM technology stocks' stats indicate high volatility & trading
		- ###### AT&T, MGM, IBM seem to have underperformed over the period
		""")

	if submenu == "Stock Daily Returns":
		interactive_plot(stock_df, 'Raw Stock Prices (WITHOUT NORMALIZATION)')
		
		normalize_df = normalize(stock_df)
		interactive_plot(normalize_df, 'Stock Prices (WITH NORMALIZATION)')
		st.write("""
		##### Observations:
		- ###### Amazon has been outperforming & is catching up with the index sp500 
		- ###### Amazon crossed Google during Q2/3 2017
		- ###### Normalized prices (here the prices are reset to $1 from the begining for a comparative analysis) tell a different story. Stock of Tesla had an exponential rise in the recent times & has risen more than any other stock!
		""")

		#daily returns histogram
		fig = plt.figure(figsize=(10,10))
		stocks_daily_return = daily_return(stock_df)
		stocks_daily_return.hist(figsize=(10, 10),bins=40)
		plt.show()
		st.pyplot(plt)
 	# 	plt.show()
		# st.pyplot()