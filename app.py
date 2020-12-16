import streamlit as st
# import streamlit.components.v1 as stc
from eda.stock_returns_analysis import run_stock_analysis
from eda.portfolio_allocation_analysis import run_portfolio_allocation_analysis


def main():
	st.write("<div align='center' style='background-color:#c0bf7e;padding:5px;border-radius:5px'><h4 style='color:#0e11b2'>Portfolio Allocation & Stock Returns Analysis</h4></div><br>", unsafe_allow_html=True)

	menu = ["Home","Stock Returns Analysis","Portfolio Allocation Analysis","About"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Project Overview")
		st.write("""
			### Stock data analysis
			- For investors to properly manage their portfolios, they need to visualize datasets, find useful patterns,
			and gain valuable insights such as stock daily returns and risks
			- In this project, I will use the power of Python to perform stock data visualization and stock return calculation

			### Portfolio asset allocations analysis
			- A portfolio is a collection of financial investments such as equities, ETFs, fixed income securities, cash,
			mutual funds, etc.
			- Per the Modern Portfolio Theory by Harry Markowitz, an efficient portlio should be constructed which diversifies
			the investments across assets to minimize the risks
			- Asset allocation is an investment strategy that is used to allocate client's assets based on their risk tolerance,
			target returns, and investent time horizon
			- The goal of the portfolio manager is to maximize returns & minimize risks - to find the optimum portfolio
			- In this project, let's assume if you have $1mn to invest in the market - how best to allocate your investments among
			selected set of securities?

			#### Datasource
				- I have downloaded the closing prices of 8 stocks & SP500 index over past 9 years (from 2012 to 2020 August)
				- Stocks: Apple, Boeing, MGM Resorts Interational, Amazon, IBM, Tesla Motors, Google
				- Source: Yahoo! Finance
			#### App Content
				- Stock Returns Analysis
				- Portfolio Asset Allocation Analysis
			#### Disclaimer
				- The raw stock prices are split-adjusted
			""")

	elif choice == "Stock Returns Analysis":
		run_stock_analysis()

	elif choice == "Portfolio Allocation Analysis":
		run_portfolio_allocation_analysis()

	else:
		st.subheader("Developed by Yuvraj Pandya")
		html = f"<a href='https://www.linkedin.com/in/yuvraj-pandya'><img src='https://github.com/yuvrajpandya/ScikitLearn/raw/master/linkedin-icon.png'/></a>"
		st.markdown(html, unsafe_allow_html=True)

		st.write("""- By harnessing the power of Data Science & AI/ML, we can optimize processes, derive actionable insights, reduce costs, and enhance customer satisfaction""")
		st.write("""- What's next? I will build predictive models using simple ML regression algorithms & Deep Neural Networks for stock price predictions""")

		appreciation = st.button("Hit to show your appreciation for my work! Thank you!")
		if appreciation:
			st.balloons()


if __name__ == '__main__':
	main()	