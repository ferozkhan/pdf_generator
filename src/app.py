"""Main application file."""
import logging
import os
import tempfile
import zipfile

from flask import Flask, render_template_string, request, send_from_directory, send_file
from flask_sqlalchemy import SQLAlchemy
from weasyprint import HTML

app = Flask(__name__)
app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['CLIENT_PDF'] = os.path.dirname(
    os.path.realpath(__file__)) + '/client_pdf'
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


def generate_pdf(url, location, filename, ext='.pdf'):
    """
    generate pdf document

    :param location:
    :param filename:
    :param ext:
    :param url: valid url with http/https
    :return:
    """
    HTML(url).write_pdf(os.path.join(location, str(filename) + ext))


def prepare_zip(zipname, zip_dir):
    log.info("writing zip.")
    with zipfile.ZipFile(zipname, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(zip_dir):
            for file in files:
                if file.endswith("pdf"):
                    zf.write(os.path.join(root, file))


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

    tmp_dir = tempfile.gettempdir()
    for filename, url in enumerate(urls):
        generate_pdf(url, tmp_dir, filename)

    prepare_zip('pdfs.zip', tmp_dir)
    return send_file(
        os.path.join(tmp_dir, "pdfs.zip"),
        attachment_filename='pdfs.zip',
        as_attachment=True
    )


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
