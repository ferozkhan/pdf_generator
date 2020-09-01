import json
import os

import pytest


@pytest.fixture
def invoice_data():
    _dirname = os.path.dirname(__file__)
    with open(f'{_dirname}/data/invoice.json') as f:
        return json.load(f)
