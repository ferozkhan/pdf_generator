import random

from ..invoice_generator import get_invoice_template, generate_invoice
from collections import namedtuple
from datetime import datetime


def test_invoice_html_template():
    res = get_invoice_template()
    assert 'Date:' in res
    assert 'Number:' in res


def test_invoice_data():
    invoice_number = random.randrange(1000, 2000)
    today = datetime.today()
    invoice = namedtuple("invoice", "number"
                                    " date")
    invoice.date = today
    invoice.number = invoice_number
    res = generate_invoice(invoice)

    assert f'Number: {invoice.number}' in res
    assert f'Date: {invoice.date}' in res
