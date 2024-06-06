from models.black_scholes_merton import BlackScholesMertonModel

class ImpliedVolatility(BlackScholesMertonModel):
    def __init__(self, option_type, S, K, r, t, q, mkt_price):
        super().__init__(option_type, S, K, r, t, 0, q)  
        self.__mkt_price__ = float(mkt_price)

    def calculate_implied_volatility(self):
        num_iter = 1000
        vol_guess = 0.3
        tol = 0.00001

        for _ in range(num_iter):
            self.__sigma__ = vol_guess

            d1, d2 = self.calculate_d1_d2()
            N_values = self.calculate_N_values(d1, d2)

            if self.option_type in ['c', 'call']:
                bs_price = self.calculate_call_price(N_values[0], N_values[2])
            else:
                bs_price = self.calculate_put_price(N_values[3], N_values[4])

            vega_calc = self.calculate_vega(N_values[1]) * 100

            if vega_calc == 0:
                return None  # Vega is 0, so we cannot proceed further.

            vol_new = vol_guess - (bs_price - self.__mkt_price__) / vega_calc

            if abs(vol_guess - vol_new) < tol:
                return vol_new * 100

            vol_guess = vol_new

        return None  # Return None if no solution is found within the iterations
    
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
    def mkt_price(self):
        return self.__mkt_price__

    @property
    def output_data(self):
        data = {'implied_volatility': self.calculate_implied_volatility()}
        return data
