from alpha_vantage.timeseries import TimeSeries

api_key = input("Enter your Alpha Vantage API Key: ")

ts = TimeSeries(key=api_key)

stock_to_search = input("Please enter the stock's ticker: ")

# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_monthly_adjusted(stock_to_search)

print(data.keys())