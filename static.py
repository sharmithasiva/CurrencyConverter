from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')

# Predefined static exchange rates (base currency: USD)
exchange_rates = {
    "USD": 1.0,
    "EUR": 0.85,
    "INR": 74.5,
    "GBP": 0.75,
    "JPY": 110.0,
    "AUD": 1.3,
    "CAD": 1.25,
    "SGD": 1.35,
    "CNY": 6.45,
    "CHF": 0.92,
    "KRW": 1185.0,
    "TRY": 8.5
}

# Predefined currency symbols
currency_symbols = {
    "USD": "$",
    "EUR": "€",
    "INR": "₹",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    "SGD": "S$",
    "CNY": "¥",
    "CHF": "Fr",
    "KRW": "₩",
    "TRY": "₺"
}

@app.route('/')
def index():
    return render_template('index.html', result=None, error=None, information=None)

@app.route('/convert', methods=['POST'])
def convert_currency():
    try:
        # Get inputs from the user
        amount = float(request.form['amount'])
        from_currency = request.form['fromCurrency']
        to_currency = request.form['toCurrency']

        # Validate currencies
        if from_currency not in exchange_rates or to_currency not in exchange_rates:
            raise ValueError("Invalid currency code!")

        # Perform currency conversion
        amount_in_usd = amount / exchange_rates[from_currency]
        converted_amount = amount_in_usd * exchange_rates[to_currency]

        # Get currency symbols
        sym_from = currency_symbols.get(from_currency, "")
        sym_to = currency_symbols.get(to_currency, "")

        # Prepare result text
        result_text = f"{sym_from} {amount} is converted to {sym_to} {round(converted_amount, 2)}"

        return render_template('index.html', result=result_text, error=None, information=None)
    except Exception as e:
        return render_template('index.html', result=None, error=str(e), information=None)

@app.route('/information', methods=['POST'])
def info():
    try:
        cur = request.form['currencyInput']
        currency_info = {
            "INR": "The Indian Rupee (INR) is the official currency of India, symbolized by ₹.",
            "USD": "The United States Dollar (USD) is the official currency of the USA, symbolized by $.",
            "EUR": "The Euro (EUR) is the official currency of the Eurozone, symbolized by €.",
            "GBP": "The British Pound Sterling (GBP) is symbolized by £.",
            "JPY": "The Japanese Yen (JPY) is symbolized by ¥.",
            "AUD": "The Australian Dollar (AUD) is symbolized by A$.",
            "CAD": "The Canadian Dollar (CAD) is symbolized by C$.",
            "SGD": "The Singapore Dollar (SGD) is symbolized by S$.",
            "CNY": "The Chinese Yuan (CNY) is symbolized by ¥.",
            "CHF": "The Swiss Franc (CHF) is symbolized by Fr.",
            "KRW": "The South Korean Won (KRW) is symbolized by ₩.",
            "TRY": "The Turkish Lira (TRY) is symbolized by ₺."
        }
        information = currency_info.get(cur, "Currency information not available.")
        return render_template('index.html', information=information, result=None, error=None)
    except Exception as e:
        return render_template('index.html', information=None, result=None, error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
