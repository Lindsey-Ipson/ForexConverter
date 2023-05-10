from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import requests
from babel import numbers
from convert import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ImASecretKey'

toolbar = DebugToolbarExtension(app)

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def showHomepage():
    """Display home page with form for client to fill out desired conversion currencies and amount"""

    return render_template('homepage.html')

@app.route('/result')
def showResult():
    """Display the conversion result from user's input, or redirect to the homepage with a flash message telling the user what went wrong"""

    from_curr = request.args.get('from-curr').upper()
    to_curr = request.args.get('to-curr').upper()
    amount = request.args.get('amount')

    if validate_curr_code(from_curr) == 'invalid':
        flash(f'{from_curr} is not a valid currency code.')
        return redirect('/')
    if validate_curr_code(to_curr) == 'invalid':
        flash(f'{to_curr} is not a valid currency code.')
        return redirect('/')

    url = f'https://api.exchangerate.host/convert?from={from_curr}&to={to_curr}&amount={amount}'

    resp = requests.get(url)
    data = resp.json()

    result = round(data['result'], 2)

    curr_symbol = numbers.get_currency_symbol(to_curr, 'en_US')

    return render_template('result.html', result=result, curr_symbol=curr_symbol)
