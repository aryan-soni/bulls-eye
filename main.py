from alpha_vantage.timeseries import TimeSeries

api_key = input("Enter your Alpha Vantage API Key: ")
ts = TimeSeries(key=api_key)

stock_to_search = input("Please enter the stock's ticker: ")

# Get json objects with the intraday data and another with the call's metadata
data, meta_data = ts.get_monthly_adjusted(stock_to_search)
index_data, index_meta_data = ts.get_monthly_adjusted("SPY")


class Stock:
    """ Models a Stock based on all its historic data.

Attributes:
    stock_data: A dictionary containing the stock's historical data.
    months_of_data: The number of months of data that the stock has.
    years_of_data: The number of years of data that the stock has.
    total_returns: A list containing the stock's total returns month-over-month 
        for 5 years.
    mean: The stock's mean return over 5 years.
    deviations: A list containing the deviations between the stock's 
        month-over-month returns over 5 years and the stock's mean return over 
        5 years.
"""

    def __init__(self, stock_data):
        """Constructs Stock using stock's and index's historical data.

        Args:
          stock_data: A dictionary containing the stock's historical data.
        """
        self.stock_data = stock_data

        self.months_of_data = len(list(self.stock_data.keys())) - 1
        self.years_of_data = self.months_of_data // 12

        self.total_returns = []
        self.deviations = []

        # Populate returns list for stock.
        if self.years_of_data >= 5:
            for i in range(0, 61):
                self.total_returns.append(self.calculate_month_return(i + 1))
        else:
            for i in range(0, self.months_of_data):
                self.total_returns[i].append(self.calculate_month_return(i + 1))

        self.mean = 0

        if self.years_of_data >= 5:
            self.mean = sum(self.total_returns) / 5
        else:
            self.mean = sum(self.total_returns) / self.years_of_data

        # Populate deviations list for stock.
        if self.years_of_data >= 5:
            for i in range(0, 61):
                self.deviations.append(self.total_returns[i] - self.mean)
        else:
            for i in range(0, self.months_of_data):
                self.deviations.append(self.total_returns[i] - self.mean)

    def calculate_month_return(self, end_index=1):
        """ Determines a stock's total return (%) for a given month

        Args:
            end_index: Where the parent keys in self.stock_data are converted 
                to a list, end_index represents which index the "end month" 
                would be. The "end month" is the month which you use to 
                calculate the "end price." For example, if you were to calculate 
                your return for the month of April, your end month would be 
                April, as you would look at the data from the end of April to
                calculate the "end price." In this context. the "start month" 
                would be March, as you would look to the data from the end of March 
                to calculate the "start price." Moving on, the end_index is set 
                to 1 by default as index 1 will store the most recent month with
                complete historical data.

        Returns:
            The actual rate of return for a given month (%) 
        """

        end_index = end_index
        start_index = end_index + 1 # Start index is 1 month before the end_index

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

class Calculator:
    """ Models a calculator that can return the key historical measures of a stock (alpha, beta etc.).

Attributes:
    stock: The stock which will be examined.
    index: The index to compare the stock to.
    beta: The beta of the stock
"""
    def __init__(self, stock, index):
        """Constructs Calculator using the stock and the index.

        Args:
          stock_data: A dictionary containing the stock's historical data.
        """
        self.stock = stock
        self.index = index

