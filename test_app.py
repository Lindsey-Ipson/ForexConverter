from app import app
from unittest import TestCase
from babel import numbers
import requests

# Make Flask errors real errors, rahter than HTML pages with error info
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    def setUp(self):

        self.client = app.test_client()

    def test_homepage(self):
        """Make sure information displays correctly at homepage"""

        with self.client:
            response = self.client.get('/')
            self.assertIn(b'<h1>Foreign Exchange Converter', response.data)
            self.assertIn(b'<form method="GET" action="/result">', response.data)
            self.assertIn(b'<input name="from-curr"', response.data)
            self.assertIn(b'<button class="convert">', response.data)

    def test_results_valid(self):
        """Test correct results from valid inputs, USD, USD, and 12"""

        with self.client:
            response = self.client.get('/result?from-curr=USD&to-curr=USD&amount=12')
            from_curr = response.request.args.get('from-curr').upper()
            to_curr = response.request.args.get('to-curr').upper()
            amount = response.request.args.get('amount')
            url = f'https://api.exchangerate.host/convert?from={from_curr}&to={to_curr}&amount={amount}'

            resp = requests.get(url)
            data = resp.json()
            result = round(data['result'], 2)
            curr_symbol = numbers.get_currency_symbol(to_curr, 'en_US')

            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(from_curr, 'USD')
            self.assertEqual(to_curr, 'USD')
            self.assertEqual(amount, '12')
            self.assertEqual(url, 'https://api.exchangerate.host/convert?from=USD&to=USD&amount=12')
            self.assertEqual(result, 12)
            self.assertEqual(curr_symbol, '$')
            self.assertIn('<span class=result>$12', html)


    def test_results_invalid(self):
        """Test proper redirection from invalid currency code input, ZZZ"""

        with self.client:
            response = self.client.get('/result?from-curr=ZZZ&to-curr=USD&amount=12')

            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')

            new_response = self.client.get(response.location)
            html = new_response.get_data(as_text=True)

            self.assertEqual(new_response.status_code, 200)
            self.assertIn('<p class="msg">ZZZ is not a valid currency code.', html)


