import json
import os
import tempfile

import pytest
from flaskr import flaskr


@pytest.fixture
def invoice_data():
    _dirname = os.path.dirname(__file__)
    with open(f'{_dirname}/data/invoice.json') as f:
        return json.load(f)


@pytest.fixture
def client():
    _db, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
    flaskr.app.config['TESTING'] = True

    with flaskr.app.test_client() as client:
        with flaskr.app.app_context():
            flaskr.init_db()
        yield client

    os.close(_db)
    os.unlink(flaskr.app.config['DATABASE'])
