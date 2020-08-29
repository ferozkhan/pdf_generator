import os

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def invoice_template():
    return render_template("invoice_v1.html")


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
