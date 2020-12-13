from alpha_vantage.timeseries import TimeSeries

api_key = input("Enter your Alpha Vantage API Key: ")
ts = TimeSeries(key=api_key)

stock_to_search = input("Please enter the stock's ticker: ")

# Get json object with the intraday data and another with the call's metadata
data, meta_data = ts.get_monthly_adjusted(stock_to_search)


class Stock:
    """ Models a Stock based on all its historic data, and contains methods that return key indicators.

Attributes:
    stock_data: A dictionary containing the stock's historical data.
"""

    def __init__(self, stock_data):
        """Constructs Stock using stock's historical data.

        Args:
          stock_data: A dictionary containing the stock's historical data.
        """
        self.stock_data = stock_data

    def get_year_return(self, end_index=1):
        """ Determines a stock's total return (%) for a given year

        Args:
            end_index: Where the parent keys in self.stock_data are converted 
                    to a list, end_index represents which index the "end month" 
                    would be. The "end month" is the month which you use to 
                    calculate the "end price." For example, if you were to calculate 
                    your return for the year from Nov. 2019-Nov. 2020, your end month 
                    would be Oct. 2020, as you would look at the data from the end of 
                    Oct. to calculate the "end price." In this context, the "start 
                    month" would be Oct. 2019, as you would look to the data from the 
                    end of Oct. to calculate the "start price." Moving on, the end_index 
                    is set to 1 by default as index 1 will store the most recent month
                    with complete historical data.

        Returns:
            The actual rate of return for a given year (%) 
        """

        end_index = end_index
        start_index = end_index + 12  # Start index is 12 months before the end_index

        # Isolate dates corresponding to end and start months, which will be a
        # string that will be used as a key.
        end_key = list(self.stock_data.keys())[end_index]
        start_key = list(self.stock_data.keys())[start_index]

        # Isolate adjusted price for the end of the end month, and the initial price
        # from the end of the start month (ensure dividend is removed).
        adjusted_end_price = float(
            self.stock_data[end_key]["5. adjusted close"])
        start_price = float(self.stock_data[start_key]["5. adjusted close"]) - float(
            self.stock_data[start_key]["7. dividend amount"])

        total_returns = (
            (adjusted_end_price - start_price) / start_price) * 100

        return total_returns

    def get_five_year_mean_return(self):
        """ Determines the mean of a stock's total returns (%) for the last five years

        Returns:
            The mean actual rate of return over five years (%) 
        """

        months_of_data = len(list(self.stock_data.keys())) - 1
        years_of_data = months_of_data // 12

        total_sum = 0
        mean = 0

        if years_of_data >= 5:

            for i in range(0, 5):
                total_sum += self.get_year_return(12 * i + 1)

            mean = total_sum / 5

        else:

            for i in range(0, years_of_data):
                total_sum += self.get_year_return(12 * i + 1)

            mean = total_sum / years_of_data

        return mean

#test_stock = Stock(data)

#print(data)
#print(test_stock.get_five_year_mean_return())
