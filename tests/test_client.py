from datasmoothie.client import Client

def test_incorrect_token():
    client = Client(api_key='incorrect')
    resp = client.request('datasource')
    assert(resp['detail'] == 'Invalid token.')


def test_new_client(token):
    client = Client(api_key=token)
    resp = client.request('datasource')
    assert('results' in resp)
