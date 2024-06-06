from flask import Blueprint, render_template, request
from models.black_scholes_merton import BlackScholesMertonModel
from models.implied_volatility import ImpliedVolatility

views = Blueprint('views', __name__)
@views.route('/')
def home():
    '''
    Responds to the root URL and renders the index.html template.

    Returns
    -------
    str
        Rendered template for the home page.
    '''
    return render_template('index.html')


@views.route('/black_scholes_merton', methods=['GET', 'POST'])
def black_scholes_merton():
    '''
    Renders the Black-Scholes-Merton option pricing form and handles 
    the calculation of option metrics upon form submission.

    Returns
    -------
    str
        Rendered template for the Black-Scholes-Merton option pricing page.
    '''
    '''if request.method == 'POST':'''
    option_type = request.args.get('option_type', 'call')
    S = request.args.get('S', 100)
    K = request.args.get('K', 100)
    r = request.args.get('r', 5)
    t = request.args.get('t', 182.5)
    sigma = request.args.get('sigma', 20)
    q = request.args.get('q', 0)
    data = BlackScholesMertonModel(option_type, S, K, r, t, sigma, q)

  
    return render_template('black_scholes_merton.html', data=data)

@views.route('/implied_volatility', methods=['GET', 'POST'])
def implied_volatility():
    '''
    Renders the Implied Volatility form and handles the calculation 
    of implied volatility using Newton-Raphson method upon form submission.

    Returns
    -------
    str
        Rendered template for the Implied Volatility calculation page.
    '''    
    option_type = request.args.get('option_type', 'c')
    S = request.args.get('S', 100)
    K = request.args.get('K', 100)
    q = request.args.get('q', 5)
    r = request.args.get('r', 5)
    t = request.args.get('t', 182.5)
    mkt_price = request.args.get('mkt_price', 5) 
    data = ImpliedVolatility(option_type, S, K, r, t, q, mkt_price)

    return render_template('implied_volatility.html', data = data)
