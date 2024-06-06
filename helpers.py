from flask import request


def get_input(request):
    """
    Extracts and processes option pricing parameters from a Flask request object.

    Reads form data from a Flask request, normalizes the data, and
    returns the relevant parameters for option pricing calculations. It supports
    different sets of parameters based on the available form data.

    Parameters
    ----------
    request : Flask request object
        The request object from which to extract form data.

    Returns
    -------
    tuple
        A tuple containing the extracted and processed parameters.
        The content of the tuple varies depending on the available form data.
        It may contain:
        - option_type (str): The type of option ('call' or 'put').
        - S (float): Current stock price.
        - K (float): Strike price.
        - r (float): Annualized risk-free interest rate, expressed as a decimal.
        - t (float): Time to expiration, expressed in years. If greater than 2, it's assumed to be in days and is converted to years.
        - sigma (float, optional): Volatility of the underlying asset, expressed as a decimal. Included if 'sigma' is in the form data.
        - q (float, optional): Dividend yield, expressed as a decimal. Included if 'q' is in the form data.
        - N and M (int, optional): Parameters for certain option pricing models. Included if both 'N' and 'M' are in the form data.
        - n (int, optional), u (float, optional), d (float, optional): Parameters for the binomial model (number of steps, up factor, down factor). Included if both 'n' and 'u' are in the form data.

    Notes
    -----
    The function normalizes interest rates, dividend yields, and volatility values by converting percentages to decimals.
    It also adjusts the Time to expiration based on the input format (years or days).
    """
    option_type = request.form.get('option_type').lower()
    
    S = float(request.form.get('S'))
    
    K = float(request.form.get('K'))
    
    r = float(request.form.get('r'))
    r = r / 100
    
    t = float(request.form.get('t'))
    if t > 1: # Assumption that any input higher than 1 means the user inputted time in days instead of years
        t = t /365
    
    sigma = None
    
    if 'sigma' in request.form:
        sigma = float(request.form.get('sigma'))
        sigma = sigma / 100
    
    if 'q' in request.form:
        q = float(request.form.get('q'))
        q = q / 100
 

    if 'N' in request.form and 'M' in request.form:
        N = int(request.form.get('N'))
        M = int(request.form.get('M'))
        return option_type, S, K, r, t, sigma, N, M
    elif 'n' in request.form and 'u' in request.form:
        n = int(request.form.get('n'))
        u = float(request.form.get('u'))
        d = 1 / u
        return option_type, S, K, r, t, n, u, d
    else:
        return option_type, S, K, r, t, sigma, q
