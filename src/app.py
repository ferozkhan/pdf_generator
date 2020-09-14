"""Main application file."""

import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)


@app.route('/pdf')
def get_pdf():
    """
    generate invoice url and return pdf
    :return: str
    """
    return ''


@app.route('/invoice')
def get_invoice():
    """
    generate invoice url and return
    :return: str
    """
    return ''


@app.route('/')
def invoice_template():
    """
    :return: str
    """
    return render_template("invoice_v1.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
