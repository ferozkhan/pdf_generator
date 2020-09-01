"""Unit tests for invoice generator."""

import os
import random
from collections import namedtuple
from datetime import datetime

from ..invoice_generator import (generate_invoice, get_invoice_template,
                                 prepare_invoice)


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
    res = prepare_invoice(invoice)

    assert f'Number: {invoice.number}' in res
    assert f'Date: {invoice.date}' in res


def test_invoice_is_generated(tmpdir, invoice_data):
    today = str(datetime.today().date())
    invoice = namedtuple("invoice", "number"
                                    " date")
    invoice.date = invoice_data.get('data')
    invoice.number = invoice_data.get('number')
    res = prepare_invoice(invoice)
    invoice_name = f'invoice_{today}_{invoice.number}.pdf'
    generate_invoice(res, tmpdir, invoice_name)
    assert invoice_name in os.listdir(tmpdir)
