"""prompt.py: Organizes user input to test the bulls_eye.py module."""

__author__      = "Aryan Soni"

from alpha_vantage.timeseries import TimeSeries
import bulls_eye

api_key = input("Enter your Alpha Vantage API Key: ")
ts = TimeSeries(key=api_key)

quandl_key = input("Enter your Quandl API Key: ")

bulls_eye.set_quandl_api_key(quandl_key)

stock_to_search = input("Please enter the stock's ticker: ")

# Get json objects with the intraday data and another with the call's metadata
data, meta_data = ts.get_monthly_adjusted(stock_to_search)
index_data, index_meta_data = ts.get_monthly_adjusted("SPY")

stock = bulls_eye.Stock(data)
index = bulls_eye.Stock(index_data)
calculator = bulls_eye.Calculator(stock, index)

print(round(calculator.beta, 2))
print(round(calculator.alpha, 2))
print(round(calculator.r_squared, 2))
print(round(calculator.standard_deviation, 2))
print(round(calculator.sharpe_ratio, 2))
