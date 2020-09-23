"""Main application file."""
import logging
import os
import tempfile
import time

from flask import Flask, request, render_template_string, send_from_directory
from flask_sqlalchemy import SQLAlchemy

from weasyprint import HTML

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['CLIENT_PDF'] = os.path.dirname(os.path.realpath(__file__)) + '/client_pdf'
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


def generate_pdf(url, location, filename):
    """
    generate pdf document

    :param url: valid url with http/https
    :return:
    """
    HTML(url).write_pdf(os.path.join(location, filename))


@app.route('/pdf')
def get_pdf():
    """
    generate invoice url and return pdf
    :return: str
    """
    urls = [location for location in request.args.get('location', '').split(' ') if location]
    url = urls[0]
    log.info(f"Receive {urls}")
    if not url:
        log.error("Locations not provided.")
        return render_template_string(FORM, errors="Missing locations.")

    tmp_dir = tempfile.gettempdir()
    filename = f"{str(time.time())}.pdf"

    generate_pdf(url, tmp_dir, filename)
    return send_from_directory(tmp_dir,
                               filename=filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
