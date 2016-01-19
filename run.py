# coding=utf-8
import argparse

from flask import render_template
from app import create_app

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# Create the flask app.
app = create_app()

@app.errorhandler(400)
def page_not_found(error):
    return render_template('errors/400.html'), 400

# Define custom filters
def thousands_seperator(number):
    return '{0:,}'.format(number)

def to_currency(number):
    return '€ {:,.2f}'.format(number)

# Register custom filters
app.jinja_env.filters['thousands_seperator'] = thousands_seperator
app.jinja_env.filters['to_currency'] = to_currency

# Run the app
if __name__ == '__main__':

    # Define the arguments.
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to: [%(default)s].')
    parser.add_argument('--port', type=int, default=app.config['SERVER_PORT'], help='Port to listen to: [%(default)s].')
    parser.add_argument('--debug', action='store_true', default=False, help='Debug mode: [%(default)s].')

    # Parse arguemnts and run the app.
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
