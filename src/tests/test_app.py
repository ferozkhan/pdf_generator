
class AppResponse:
    OK = 200


def test_app_home_response_is_ok(client):
    response = client.get('/')
    assert response.status_code == AppResponse.OK


def test_app_home_response_has_form(client):
    response = client.get('/').get_data()
    assert b'<form action="/pdf">' in response
