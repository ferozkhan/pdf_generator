"""Main application file."""
import asyncio
import logging
import os
import pathlib
import tempfile
import zipfile
from typing import Union

from weasyprint import HTML

from flask import (Flask, render_template_string, request, send_file,
                   send_from_directory)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['CLIENT_PDF'] = os.path.dirname(
    os.path.realpath(__file__)) + '/client_pdf'
db = SQLAlchemy(app)

log = logging.getLogger(__name__)
loop = asyncio.get_event_loop()

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


async def generate_pdf(url, location, filename, ext='.pdf'):
    """
    generate pdf document

    :param location:
    :param filename:
    :param ext:
    :param url: valid url with http/https
    :return:
    """
    await HTML(url).write_pdf(os.path.join(location, str(filename) + ext))


def prepare_zip(zipname, zip_dir):
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(zip_dir):
            for file in files:
                if file.endswith("pdf"):
                    zf.write(os.path.join(root, file))


def get_html(url: str) -> HTML:
    return HTML(url)


def prepare_pdf():
    pass


@app.route('/pdf')
def get_pdf():
    """
    generate invoice url and return pdf
    :return: str
    """
    urls = [location for location in request.args.get(
        'location', '').split(' ') if location]
    log.info(f"Receive {urls}")
    if not urls:
        log.error("Locations not provided.")
        return render_template_string(FORM, errors="Missing locations.")

    prepare_pdf()
    tmp_dir = tempfile.gettempdir()
    for filename, url in enumerate(urls):
        loop.run_until_complete(generate_pdf(url, tmp_dir, filename))

    log.info("writing zip.")
    prepare_zip('pdfs.zip', tmp_dir)
    return send_file(
        os.path.join(tmp_dir, "pdfs.zip"),
        attachment_filename='pdfs.zip',
        as_attachment=True
    )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
