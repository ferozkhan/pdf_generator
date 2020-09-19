import json
import os

import pytest
from flask import app
from flask.testing import FlaskClient



@pytest.fixture
def invoice_data():
    _dirname = os.path.dirname(__file__)
    with open(f'{_dirname}/data/invoice.json') as f:
        return json.load(f)


class TestClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@pytest.fixture
def client():
    app.test_client_class = TestClient
    return app.test_client()
