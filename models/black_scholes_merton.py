import math
from scipy.stats import norm

class BlackScholesMertonModel:
    '''
    Calculate theoretical option prices using the Black-Scholes-Merton model.

    Black-Scholes-Merton model is a differential equation widely used for pricing European option contracts. 
    It requires five input variables: the strike price, stock price, time to expiration, risk-free rate, and volatility of the underlying asset.

    Parameters
    ----------
    option_type : str
        Type of the option ('c' or 'call' for call option, 'p' or 'put' for put option).
    S : float
        Stock price.
    K : float
        Strike price of the option.
    r : float
        Annual risk-free interest rate, expressed as a decimal.
    t : float
        Time to expiration of the option, in days .
    sigma : float
        Annual volatility of the underlying asset, expressed as a decimal.
    q : float
        Continuously compounded dividend yield, expressed as a decimal.
    '''
    def __init__(self, option_type, S, K, r, t, sigma, q):
        self.__option_type__ = option_type
        self.__S__ = float(S)
        self.__K__ = float(K)
        self.__q__ = float(q)/100
        self.__r__ = float(r)/100 
        self.__t__ = float(t)/365
        self.__sigma__ = float(sigma)/100 

    def calculate_d1_d2(self):
        '''
        Calculate d1 and d2 for later use in option pricing formulas.

        Returns
        -------
        tuple
            Tuple containing d1 and d2 values.
        '''
        if self.__t__ == 0:
            return float('inf'), float('inf')
        else:
            d1 = (math.log(self.__S__ / self.__K__) + (self.__r__ - self.__q__ + (self.__sigma__**2) / 2) * self.__t__) / (self.__sigma__ * math.sqrt(self.__t__))
            d2 = d1 - self.__sigma__ * math.sqrt(self.__t__)
            return d1, d2

    def calculate_N_values(self, d1, d2):
        '''
        Calculate various N values for option pricing.

        Parameters
        ----------
        d1 : float
            The d1 value.
        d2 : float
            The d2 value.

        Returns
        -------
        tuple
            Tuple containing N_d1, N_d1_gamma_theta_vega, N_d2, N_neg_d1, N_neg_d2 values.
        '''
        N_d1 = norm.cdf(d1)
        N_d1_gamma_theta_vega = norm.pdf(d1)
        N_d2 = norm.cdf(d2)
        N_neg_d1 = norm.cdf(-d1)
        N_neg_d2 = norm.cdf(-d2)
        return N_d1, N_d1_gamma_theta_vega, N_d2, N_neg_d1, N_neg_d2

    def calculate_call_price(self, N_d1, N_d2):
        '''
        Calculate call option price.

        Parameters
        ----------
        N_d1 : float
            N_d1 value - The probability that a standard normal random variable is less than or equal to d1.
        N_d2 : float
            N_d2 value - The probability that a standard normal random variable is less than or equal to d2.

        Returns
        -------
        float
            Call option price.
        '''
        if self.__t__ == 0:
            return max(0, self.__S__ - self.__K__)
        else:
            return (N_d1 * self.__S__ * math.exp(- self.__q__ * self.__t__))- (N_d2 * self.__K__ * math.exp(-self.__r__ * self.__t__))

    def calculate_put_price(self, N_neg_d1, N_neg_d2):
        '''
        Calculate put option price.

        Parameters
        ----------
        N_neg_d1 : float
            N_neg_d1 value - The probability that a standard normal random variable is greater than -d1.
        N_neg_d2 : float
            N_neg_d2 value - The probability that a standard normal random variable is greater than -d2.

        Returns
        -------
        float
            Put option price.
        '''
        if self.__t__ == 0:
            return max(0, self.__K__ - self.__S__)
        else:
            return self.__K__ * math.exp(-self.__r__ * self.__t__) * N_neg_d2 - self.__S__ * math.exp(-self.__q__ * self.__t__)* N_neg_d1

    def calculate_delta(self, N_d1, N_neg_d1):
        '''
        Calculate the delta value, a measure of option sensitivity to changes in the underlying asset price.

        Parameters
        ----------
        N_d1 : float
            N_d1 value - The probability that a standard normal random variable is less than or equal to d1.
        N_neg_d1 : float
            N_neg_d1 value - The probability that a standard normal random variable is greater than -d1.

        Returns
        -------
        float
            Delta value.
        '''
        if self.__t__ == 0: # As per "Sheldon Natenberg: Option Volatility and Pricing"
            if self.__S__ == self.__K__:
                return {'call':0.5, 'put':-0.5}[self.__option_type__]
            elif self.__S__ > self.__K__:
                    return {'call':1, 'put':0}[self.__option_type__]
            else:
                    return {'call':0, 'put':1}[self.__option_type__]
        else:
            if self.option_type in ['c', 'call']:
                return N_d1 * math.exp(-self.__q__ * self.__t__)
            elif self.option_type in ['p', 'put']:
                return -N_neg_d1 * math.exp(-self.__q__ * self.__t__)
        return 0
        

    def calculate_gamma(self, N_d1_gamma_theta_vega):
        '''
        Calculate the gamma value, a measures of rate of change of the option's Delta with respect to a move in the underlying asset.

        Parameters
        ----------
        N_d1_gamma_theta_vega : float
            N_d1_gamma_theta_vega value - The probability that a standard normal random variable is less than or equal to d1.

        Returns
        -------
        float
            Gamma value.
        '''
        if self.__t__ == 0:
            return 0 # Gamma becomes 0 as there's no time for delta to change
        return math.exp(-self.__q__ * self.__t__) * N_d1_gamma_theta_vega / (self.__S__ * self.__sigma__ * math.sqrt(self.__t__))

    def calculate_theta(self, N_d1, N_d1_gamma_theta_vega, N_neg_d1, N_d2, N_neg_d2):
        '''
        Calculate the theta value, a measure of option sensitivity to time decay.

        Parameters
        ----------
        N_d1_gamma_theta_vega : float
            N_d1_gamma_theta_vega value - The probability that a standard normal random variable is less than or equal to d1.
        N_d2 : float
            N_d2 value - The probability that a standard normal random variable is less than or equal to d2.
        N_neg_d2 : float
            N_neg_d2 value - The probability that a standard normal random variable is greater than -d2.

        Returns
        -------
        float
            Theta value.
        '''
        if self.__t__ == 0:
            return 0 # Theta becomes irrelevant at t = 0
        else:
            if self.option_type in ['c', 'call']:
                theta = -(self.__S__  * math.exp(-self.__q__ * self.__t__) * self.__sigma__ / (2 * math.sqrt(self.__t__)) * N_d1_gamma_theta_vega) \
                        - self.__r__ * self.__K__ * math.exp(-self.__r__ * self.__t__) * N_d2 + self.__q__ * self.__S__ * math.exp(-self.__q__ * self.__t__) * N_d1
            elif self.option_type in ['p', 'put']:
                theta = -(self.__S__ * math.exp(-self.__q__ * self.__t__) * self.__sigma__ / (2 * math.sqrt(self.__t__)) * N_d1_gamma_theta_vega)\
                        + self.__r__ * self.__K__ * math.exp(-self.__r__ * self.__t__) * N_neg_d2 - self.__q__ * self.__S__ * math.exp(-self.__q__ * self.__t__) * N_neg_d1
            return theta / 365

    def calculate_vega(self, N_d1_gamma_theta_vega):
        '''
        Calculate the vega value, a measure of option sensitivity to changes in volatility.

        Parameters
        ----------
        N_d1_gamma_theta_vega : float
            N_d1_gamma_theta_vega value - The probability that a standard normal random variable is less than or equal to d1.

        Returns
        -------
        float
            Vega value.
        '''
        if self.__t__ == 0:
            return 0 # Vega becomes irrelevant at t = 0, no time left for the underlying asset's volatility to affect the option's price.
        else:
            return (self.__S__ * math.exp(-self.__q__ * self.__t__) * math.sqrt(self.__t__) * N_d1_gamma_theta_vega) / 100   # We are interested in 1% increase in volatility, thus we divide by 100

    def calculate_rho(self, N_d2, N_neg_d2):
        '''
        Calculate the rho value, a measure of option sensitivity to changes in interest rates.

        Parameters
        ----------
        N_d2 : float
            N_d2 value - The probability that a standard normal random variable is less than or equal to d2.
        N_neg_d2 : float
            N_neg_d2 value - The probability that a standard normal random variable is greater than -d2.

        Returns
        -------
        float
            Rho value.
        '''
        if self.__t__ == 0:
            return 0 # Rho becomes irrelevant at t = 0
        else:
            if self.option_type in ['c', 'call']:
                return (self.__K__ * self.__t__ * math.exp(-self.__r__ * self.__t__) * N_d2) / 100  # We are interested in 1% increase in interest rates, thus we divide by 100
            elif self.option_type in ['p', 'put']:
                return (-self.__K__ * self.__t__ * math.exp(-self.__r__ * self.__t__) * N_neg_d2) / 100 # We are interested in 1% increase in rates, thus we divide by 100

    def calculate_option_metrics(self):
        '''
        Calculate various option metrics using the Black-Scholes formulas.

        Returns
        -------
        tuple
            Tuple containing call_price, put_price, delta_value, gamma_value, theta_value, vega_value, rho_value.
        '''
        d1, d2 = self.calculate_d1_d2()
        N_d1, N_d1_gamma_theta_vega, N_d2, N_neg_d1, N_neg_d2 = self.calculate_N_values(d1, d2)

        # Call and put prices
        call_price = self.calculate_call_price(N_d1, N_d2)
        put_price = self.calculate_put_price(N_neg_d1, N_neg_d2)

        # Option "greeks"
        delta_value = self.calculate_delta(N_d1, N_neg_d1)
        gamma_value = self.calculate_gamma(N_d1_gamma_theta_vega)
        theta_value = self.calculate_theta(N_d1, N_d1_gamma_theta_vega, N_neg_d1, N_d2, N_neg_d2)
        vega_value = self.calculate_vega(N_d1_gamma_theta_vega)
        rho_value = self.calculate_rho(N_d2, N_neg_d2)
        
        data = {"call_price": call_price, 
                    "put_price": put_price, 
                    "delta_value": delta_value, 
                    "gamma_value": gamma_value,
                    "theta_value": theta_value, 
                    "vega_value": vega_value, 
                    "rho_value": rho_value}
        return data
        
    @property
    def option_type(self):
        return self.__option_type__

    @property
    def S(self):
        return self.__S__
    
    @property
    def K(self):
        return self.__K__
    
    @property
    def q(self):
        return self.__q__*100
    
    @property
    def r(self):
        return self.__r__*100
    
    @property
    def t(self):
        return self.__t__*365
    
    @property
    def sigma(self):
        return self.__sigma__*100
    
    @property
    def output_data(self):
        data = self.calculate_option_metrics()
        return data
