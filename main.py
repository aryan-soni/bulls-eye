from alpha_vantage.timeseries import TimeSeries
import quandl

api_key = input("Enter your Alpha Vantage API Key: ")
ts = TimeSeries(key=api_key)

quandl.ApiConfig.api_key = input("Enter your Quandl API Key: ")

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
    total_return: The stock's five-year total return (including dividends, but assuming 
        the dvidends aren't re-invested).
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
            for i in range(60):
                self.total_returns.append(self.calculate_month_return(i))
        else:
            for i in range(self.months_of_data):
                self.total_returns.append(self.calculate_month_return(i))

        # Determine total return over 5 years
        self.total_return = self.calculate_total_return()

        self.mean = 0

        if self.years_of_data >= 5:
            self.mean = sum(self.total_returns) / 60
        else:
            self.mean = sum(self.total_returns) / self.months_of_data

        # Populate deviations list for stock.
        if self.years_of_data >= 5:
            for i in range(60):
                self.deviations.append(self.total_returns[i] - self.mean)
        else:
            for i in range(self.months_of_data):
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
        start_index = end_index + 1  # Start index is 1 month before the end_index

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

    def calculate_total_return(self):
        """ Determines a stock's total return (%) over 5 years

        Returns:
            The actual rate of return over 5 years (%)
        """

        if self.years_of_data >= 5:
            start_index = 60
        else:
            start_index = self.months_of_data

        end_index = 1

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

        # Add dividends from entire 5 years to end price
        for i in range(2, start_index):
            selected_key = list(self.stock_data.keys())[i]
            adjusted_end_price += float(
                self.stock_data[selected_key]["7. dividend amount"])

        total_return = (
            (adjusted_end_price - start_price) / start_price) * 100

        return total_return


class Calculator:
    """ Models a calculator that can return the key historical measures of a stock (alpha, beta etc.).

Attributes:
    stock: The stock which will be examined.
    index: The index to compare the stock to.
    beta: The beta of the stock.
    risk_free_return: The risk-free rate of return.
    alpha: The alpha of the stock (specificially Jensen's alpha, as per the Capital Asset Pricing Model).
    r-squared: The r-squared of the stock when comparing it to SPY (the benchmark).
    standard_deviation: The standard deviation of the chosen stock, reflecting the spread
        of returns relative to the mean return.
"""

    def __init__(self, stock, index):
        """Constructs Calculator using the stock and the index.

        Args:
          stock_data: A dictionary containing the stock's historical data.
        """
        self.stock = stock
        self.index = index
        self.beta = self.calculate_beta()
        self.risk_free_return = self.get_risk_free_return()
        self.alpha = self.calculate_alpha()
        self.r_squared = self.calculate_r_squared()
        self.standard_deviation = self.calculate_standard_deviation()

    def calculate_covariance(self):
        """ Determines the covariance of the chosen stock and index.

        Returns:
            The covariance of the chosen stock and index.
        """

        product_of_deviations = [
            a * b for a, b in zip(self.stock.deviations, self.index.deviations)]

        sum_of_products = sum(product_of_deviations)

        if self.stock.years_of_data >= 5:
            return sum_of_products / 59
        else:
            return sum_of_products / (self.stock.months_of_data - 1)

    def calculate_variance(self):
        """ Determines the variance for the index.

        Returns:
            The variance of index.
        """

        squared_deviations = [(n) ** 2 for n in self.index.deviations]

        sum_of_squared_deviations = sum(squared_deviations)

        if self.stock.years_of_data >= 5:
            return sum_of_squared_deviations / 59
        else:
            return sum_of_squared_deviations / (self.stock.months_of_data - 1)

    def calculate_beta(self):
        """ Determines the beta for the chosen stock

        Returns:
            The beta of the chosen stock, which illustrates the expected change
                in a security's return given a 1% change in the market index.
        """

        return self.calculate_covariance() / self.calculate_variance()

    def get_risk_free_return(self):
        """ Determines the risk free rate of return (%).

        Returns:
            The risk free rate of return (%). Leverages the yield of the 5-year 
            U.S. Treasury Note; corresponding to when the 5-year period begins 
            for the stock being tracked. For example, if you're looking at MG.TO 
            and the 5-year period you're examining starts in Nov. 2015, this method 
            would return the yield for the U.S. Treasury 5-Year Note had you purchased 
            it at that specific date in Nov. 2015.
        """

        # Index in the list of months of the first month being tracked in the five-year period
        index_of_first_month = 0

        if self.stock.years_of_data >= 5:
            index_of_first_month = 60
        else:
            index_of_first_month = self.stock.months_of_data

        date = list(self.stock.stock_data.keys())[index_of_first_month]

        treasury_data = quandl.get("USTREASURY/YIELD", start_date=date,
                                   end_date=date).to_dict()

        return list(treasury_data['5 YR'].values())[0]

    def calculate_alpha(self):
        """ Determines the alpha of the chosen stock.

        Returns:
            The alpha of the chosen stock, which illustrates the difference
                between a security's return and its expected return per the
                Security Market Line.
        """

        return self.stock.total_return - self.risk_free_return - (self.beta * (self.index.total_return - self.risk_free_return))

    def calculate_r_squared(self):
        """ Determines the r-squared value of the chosen stock.

        Returns:
            The r-squared value of the chosen stock, indicating how closely the 
                stock's movements correlate with the benchmark index's (SPY).
        """

        product_of_returns = [a * b for a, b in zip(self.stock.total_returns,
                                                    self.index.total_returns)]

        sum_of_stock_returns = sum(self.stock.total_returns)
        sum_of_index_returns = sum(self.index.total_returns)

        sum_of_stock_returns_squared = sum(
            [(n**2) for n in self.stock.total_returns])
        sum_of_index_returns_squared = sum(
            [(n**2) for n in self.index.total_returns])

        # Split calculations for numerator and denominator for readability
        if self.stock.years_of_data >= 5:
            numerator = 60 * sum(product_of_returns) - sum_of_stock_returns * sum_of_index_returns
            denominator = ((60 * sum_of_stock_returns_squared - (sum_of_stock_returns ** 2)) *
                (60 * sum_of_index_returns_squared - (sum_of_index_returns ** 2))) ** 0.5
        else:
            numerator = self.stock.months_of_data * sum(product_of_returns) - sum_of_stock_returns * sum_of_index_returns
            denominator = ((self.stock.months_of_data * sum_of_stock_returns_squared - (sum_of_stock_returns ** 2)) *
                (self.stock.months_of_data * sum_of_index_returns_squared - (sum_of_index_returns ** 2))) ** 0.5            

        return numerator / denominator

    def calculate_standard_deviation(self):
        """ Determines the standard deviation of the chosen stock.

        Returns:
            The standard deviation of the chosen stock, reflecting the spread
            of returns relative to the mean return.
        """

        if self.stock.years_of_data >= 5:
            return (sum([(n ** 2) for n in self.stock.deviations]) / 59) ** 0.5
        else:
            return (sum([(n ** 2) for n in self.stock.deviations]) / (self.stock.months_of_data - 1)) ** 0.5

stock = Stock(data)
index = Stock(index_data)
calculator = Calculator(stock, index)


print(len(calculator.stock.total_returns))
print(round(calculator.beta, 2))
print(round(calculator.alpha, 2))
print(round(calculator.r_squared, 2))
print(round(calculator.standard_deviation, 2))
