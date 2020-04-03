import json

from datasmoothie import Client
from datasmoothie import Report
from datasmoothie import Datasource

def test_get_meta_and_data(token):
    client = Client(api_key=token)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    resp = datasource.get_meta_and_data()
    print(resp.keys())
    assert 'meta' in resp
    assert 'data' in resp
