#!/usr/bin/env python

"""prompt.py: Organizes user input to test the bulls_eye.py module."""

__author__      = "Aryan Soni"

from alpha_vantage.timeseries import TimeSeries
import bulls_eye

while True:

	api_key = input("Enter your Alpha Vantage API Key: ")

	try:
		ts = TimeSeries(key=api_key)
		# Try to get data for SPY
		index_data, index_meta_data = ts.get_monthly_adjusted("SPY")
	except:
		print("Please enter a valid Alpha Vantage API Key.")
		continue

	break

while True:

	quandl_key = input("Enter your Quandl API Key: ")

	# If the key is valid
	if bulls_eye.set_quandl_api_key(quandl_key):
		break
	else:
		print("Please enter a valid Quandl API key.")

while True:

	while True:
		try:
			stock_to_search = input("Please enter the stock's ticker: ")
			# Get json objects with the intraday data and another with the call's metadata
			data, meta_data = ts.get_monthly_adjusted(stock_to_search)
		except:
			print("This stock is not in the database. Please enter another ticker.")
			continue

		break

	stock = bulls_eye.Stock(data)
	index = bulls_eye.Stock(index_data)
	calculator = bulls_eye.Calculator(stock, index)

	print("\nBeta (5Y Monthly): {}".format(round(calculator.beta, 2)))
	print("Alpha (5Y Monthly): {} %".format(round(calculator.alpha, 2)))
	print("R-Squared (5Y Monthly): {}".format(round(calculator.r_squared, 2)))
	print("Standard Deviation (5Y Annually): {} %".format(round(calculator.standard_deviation, 2)))
	print("Sharpe Ratio (5Y Annually): {}".format(round(calculator.sharpe_ratio, 2)))
	
	to_continue = input("\nWould you like to enter another stock? (Y/N)\n").upper()

	if(to_continue != "Y"):
		break

print("\nThanks for using Bulls' Eye!")

