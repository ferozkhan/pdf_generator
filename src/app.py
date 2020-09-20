"""Main application file."""
import logging
import os

from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy


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


@app.route('/pdf', )
def get_pdf():
    """
    generate invoice url and return pdf
    :return: str
    """
    locations = [location for location in request.args.get('location', '').split(' ')]
    if not locations:
        log.error("Locations not provided.")
        return render_template_string(FORM, errors="Missing locations.")
    return ','.join(locations)


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
