"""Main application file."""
import logging
import os
import time

from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy

import requests
from weasyprint import HTML

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

log = logging.getLogger(__name__)

FORM = """
{% if errors %}<p>Error: {{errors}}<p>{% endif %}
<form action="/pdf">
<input type="text" name="location"/>
<input type="submit" value="generate pdf">
</form>
"""


@app.route('/')
def home():
    return render_template_string(FORM)


def generate_pdf(url):
    """
    generate pdf document

    :param url: valid url with http/https
    :return:
    """
    HTML(url).write_pdf(str(time.time()))


@app.route('/pdf')
def get_pdf():
    """
    generate invoice url and return pdf
    :return: str
    """
    locations = [location for location in request.args.get('location', '').split(' ') if location]
    log.info(f"Receive {locations}")
    if not locations:
        log.error("Locations not provided.")
        return render_template_string(FORM, errors="Missing locations.")
    for location in locations:
        generate_pdf(location)
    return f"pdf created for {locations}"


@app.route('/invoice')
def get_invoice():
    """
    generate invoice url and return
    :return: str
    """
    return ''


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
