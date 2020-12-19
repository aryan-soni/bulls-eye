import quandl

def set_quandl_api_key(key):
    """Sets the API key for Quandl.

    Args:
      key: The API key for Quandl.
    """
    quandl.ApiConfig.api_key = key

class Stock:
    """ Models a Stock based on all its historic data.

Attributes:
    stock_data: A dictionary containing the stock's historical data.
    months_of_data: The number of months of data that the stock has.
    years_of_data: The number of years of data that the stock has.
    total_return: The stock's five-year total return (including dividends, but assuming 
        the dvidends aren't re-invested).
    total_monthly_returns: A list containing the stock's total returns month-over-month
        for 5 years.
    total_annual_returns: A list containing the stock's total returns year-over-year
        for 5 years.
    mean_monthly_return: The stock's mean return over 5 years.
    mean_annual_return: The stock's mean annual return over 5 years.
    deviations_monthly_returns: A list containing the deviations between the stock's
        month-over-month returns over 5 years and the stock's mean monthly return over
        5 years.
    deviations_annual_returns: A list containing the deviations between the stock's
        annual returns over 5 years and the stock's mean annual return over
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

        self.total_monthly_returns = []
        self.total_annual_returns = []
        self.deviations_monthly_returns = []
        self.deviations_annual_returns = []

        # Populate monthly returns list for stock.
        if self.years_of_data >= 5:
            for i in range(60):
                self.total_monthly_returns.append(self.calculate_month_return(i))
        else:
            for i in range(self.months_of_data):
                self.total_monthly_returns.append(self.calculate_month_return(i))

        # Populate annual returns list for stock.
        if self.years_of_data >= 5:
            for i in range(5):
                self.total_annual_returns.append(self.calculate_year_return(i * 12 + 1))
        else:
            for i in range(self.months_of_data // 12):
                self.total_annual_returns.append(self.calculate_year_return(i * 12 + 1))

        # Determine total return over 5 years
        self.total_return = self.calculate_total_return()

        self.mean_monthly_return = 0
        self.mean_annual_return = 0

        if self.years_of_data >= 5:
            self.mean_monthly_return = sum(self.total_monthly_returns) / 60
            self.mean_annual_return = sum(self.total_annual_returns) / 5
        else:
            self.mean_monthly_return = sum(self.total_monthly_returns) / self.months_of_data
            self.mean_annual_return = sum(self.total_monthly_returns) / (self.months_of_data // 12)

        # Populate monthly deviations lists for stock.
        if self.years_of_data >= 5:
            for i in range(60):
                self.deviations_monthly_returns.append(self.total_monthly_returns[i] - self.mean_monthly_return)
        else:
            for i in range(self.months_of_data):
                self.deviations_monthly_returns.append(self.total_monthly_returns[i] - self.mean_monthly_return)

        # Populate annual deviations lists for stock.
        if self.years_of_data >= 5:
            for i in range(5):
                self.deviations_annual_returns.append(self.total_annual_returns[i] - self.mean_annual_return)
        else:
            for i in range(self.months_of_data // 12):
                self.deviations_annual_returns.append(self.total_annual_returns[i] - self.mean_annual_return)

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
            The actual rate of return for a given month (%).
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

    def calculate_year_return(self, end_index=1):
        """ Determines a stock's total return (%) for a given year

        Args:
            end_index: Where the parent keys in self.stock_data are converted
                to a list, end_index represents which index the "end month"
                would be. The "end month" is the month which you use to
                calculate the "end price." For example, if you were to calculate
                your returns from April 2019-April 2020, your end month would be
                March 2020, as you would look at the data from the end of March 2020 to
                calculate the "end price." In this context. the "start month"
                would be March 2019, as you would look to the data from the end of March
                2019 to calculate the "start price." Moving on, the end_index is set
                to 1 by default as index 1 will store the most recent month with
                complete historical data.

        Returns:
            The actual rate of return for a given year (%).
        """

        end_index = end_index
        start_index = end_index + 12 # Start index is 12 months before the end_index

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

        # Add dividends from entire year to end price
        for i in range(end_index + 1, start_index):
            selected_key = list(self.stock_data.keys())[i]
            adjusted_end_price += float(
                self.stock_data[selected_key]["7. dividend amount"])

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
    sharpe_ratio: The sharpe ratio of the chosen stock, reflecting the average return earned in excess 
        of the risk-free rate per unit of volatility.
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
        self.sharpe_ratio = self.calculate_sharpe_ratio()

    def calculate_covariance(self):
        """ Determines the covariance of the chosen stock and index.

        Returns:
            The covariance of the chosen stock and index.
        """

        product_of_deviations = [
            a * b for a, b in zip(self.stock.deviations_monthly_returns, self.index.deviations_monthly_returns)]

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

        squared_deviations = [(n) ** 2 for n in self.index.deviations_monthly_returns]

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

        product_of_returns = [a * b for a, b in zip(self.stock.total_monthly_returns,
                                                    self.index.total_monthly_returns)]

        sum_of_stock_returns = sum(self.stock.total_monthly_returns)
        sum_of_index_returns = sum(self.index.total_monthly_returns)

        sum_of_stock_returns_squared = sum(
            [(n**2) for n in self.stock.total_monthly_returns])
        sum_of_index_returns_squared = sum(
            [(n**2) for n in self.index.total_monthly_returns])

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
                of the stock's returns relative to the mean return.
        """

        if self.stock.years_of_data >= 5:
            return (sum([(n ** 2) for n in self.stock.deviations_annual_returns]) / 4) ** 0.5
        else:
            return (sum([(n ** 2) for n in self.stock.deviations_annual_returns]) / ((self.stock.months_of_data // 12) - 1)) ** 0.5


    def calculate_sharpe_ratio(self):
        """ Determines the sharpe ratio of the chosen stock.

        Returns:
            The sharpe ratio of the chosen stock, reflecting the average return earned in excess 
                of the risk-free rate per unit of volatility.
        """

        # For any given year, the risk-free rate can be divided by 5 since it describes a 5y period
        # Divide risk-free rate by 5 as you need the rate on a per year basis to estimate the excess return per year
        risk_free_rate = self.risk_free_return / 5

        return (self.stock.mean_annual_return - risk_free_rate) / self.standard_deviation