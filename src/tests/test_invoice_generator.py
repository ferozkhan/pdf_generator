import pytest
from ..invoice_generator import get_invoice_template


def test_invoice_html_template():
    res = get_invoice_template()
    assert 'invoice number' in res

