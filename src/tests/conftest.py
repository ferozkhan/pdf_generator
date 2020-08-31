import json

import pytest


@pytest.fixture
def invoice_data():
    with open('./data/invoice.json') as f:
        return json.load(f)
