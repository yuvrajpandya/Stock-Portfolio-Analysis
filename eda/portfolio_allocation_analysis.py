import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.figure_factory as ff
from modules.common import load_data,interactive_plot,normalize,daily_return

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def run_portfolio_allocation_analysis():
	# local_css('modules/style.css')
	stock_df = load_data('data/stock.csv')


	allocation_btn = st.sidebar.button('Generate allocations & recompute')

	st.header("α Generating alpha")
	st.write("Let's assume that an investor has $1mn dollars to invest.")
	st.markdown("Investor allocates their funds across 9 securities with random weights.")

	st.write("""##### Illustrative example: 
	Assets  = [AAPL BA T MGM AMZN IBM TSLA GOOG sp500]
	Weights = [10.92% 12.06% 0.602% 3.627% 14.492% 17.636% 6.492% 18.89% 15.2599%]
	Funds allocated to sp500 index = 15.2599% * $1mn = $152,599
	How much returns would this portfolio generate (inception-to-date) had investor invested since 2012?
	How risky is this portfolio?
	What is the sharpe ratio of this portfolio?""")

	st.subheader("We will compute overall portfolio value using random weights.")
	st.markdown("Using **'Generate allocations & recompute'** button in the sidebar different asset allocations can be applied which will recalculate the portfolio value. Go ahead & try out different allocations!!!")

	if allocation_btn:
		# Create random weights for the stocks and normalize them
		weights = np.array(np.random.random(9))
		weights = weights / np.sum(weights)

		d={'asset':stock_df.columns, 'weights':weights}
		weights_df = pd.DataFrame(d).round(4)
		# weights_df.style.apply(lambda x: ['background: lightgreen' for i in x], axis=1)
		st.markdown("**Portfolio weights**")
		st.dataframe(weights_df.T, height=500)
	
		st.markdown("Allocate funds per the weights & calculate portfolio daily worth & returns | Note the first record shows allocated funds")
		portfolio_df = portfolio_allocation(stock_df, weights)
		st.dataframe(portfolio_df)

		# portfolio daily worth
		interactive_plot(portfolio_df.drop(['portfolio daily worth in $', 'portfolio daily % return'], axis = 1), plot_title='Portfolio individual stocks worth in $ over time',xaxes_title='holding period',yaxes_title='stock valuations',yaxes_prefix='$')
		st.markdown("♦Notice a whopping returns in Tesla's valuations in recent times!!!")

		# Plot the portfolio daily return
		fig = px.line(x=portfolio_df.index, y=portfolio_df['portfolio daily % return'], title="Portfolio Daily % Return",width=860, height=450)
		fig.update_xaxes(dtick="M12",title_text="time horizon")
		fig.update_yaxes(title_text="daily returns")
		st.plotly_chart(fig)

		# portfolio daily returns
		fig = px.histogram(portfolio_df, x = 'portfolio daily % return')
		fig.update_xaxes(title_text="distribution of portfolio daily % returns")
		st.plotly_chart(fig)


		# portfolio stats
		st.write("""#### Summary of investor's portfolio | Investment amount $1mn | Holding period ~9 years""")

		# Cumulative return of the portfolio (Note that we now look for the last net worth of the portfolio compared to it's start value)
		cumulative_return = ((portfolio_df['portfolio daily worth in $'][-1:] - portfolio_df['portfolio daily worth in $'][0])/portfolio_df['portfolio daily worth in $'][0]) * 100
		st.markdown("Cumulative return of the portfolio is **{}%**".format(round(cumulative_return.values[0],2)))

		st.markdown("Standard deviation of the portfolio is **{}%**".format(round(portfolio_df['portfolio daily % return'].std(),2)))

		st.markdown("Average daily return of the portfolio is **{}%**".format(round(portfolio_df['portfolio daily % return'].mean(),2)))

		# Annualized sharpe ration - there are 252 trading days in a year
		sharpe_ratio = portfolio_df['portfolio daily % return'].mean() / portfolio_df['portfolio daily % return'].std() * np.sqrt(252)
		st.markdown("Sharpe ratio of the portfolio is **{}%**".format(round(sharpe_ratio,2)))




# PORTFOLIO ALLOCATION - DAILY RETURN/WORTH CALCULATION
def portfolio_allocation(df, weights):

	df_portfolio = df.copy()
  
	# Normalize the stock avalues 
	df_portfolio = normalize(df_portfolio)
  
	for counter, stock in enumerate(df_portfolio.columns):
		df_portfolio[stock] = df_portfolio[stock] * weights[counter]
		df_portfolio[stock] = round(df_portfolio[stock] * 1000000)

	df_portfolio['portfolio daily worth in $'] = df_portfolio.sum(axis = 1)
  
	df_portfolio['portfolio daily % return'] = 0.0000

	# Calculate the percentage of change from the previous day
	for i in range(1, len(df)):
		df_portfolio['portfolio daily % return'][i] = ((df_portfolio['portfolio daily worth in $'][i] - df_portfolio['portfolio daily worth in $'][i-1]) / df_portfolio['portfolio daily worth in $'][i-1]) * 100
  
	# set the value of first row to zero, as previous value is not available
	df_portfolio['portfolio daily % return'][0] = 0
	return df_portfolio

