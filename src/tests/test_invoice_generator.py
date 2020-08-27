import random

import pytest
from ..invoice_generator import get_invoice_template, generate_invoice


def test_invoice_html_template():
    res = get_invoice_template()
    assert 'invoice number' in res


def test_invoice_data():
    invoice_number = random.randrange(1000, 2000)
    res = generate_invoice(invoice_number=invoice_number)
    assert f'invoice number: {invoice_number}' == res
