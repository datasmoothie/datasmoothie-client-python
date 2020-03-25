from datasmoothie.client import Client
from datasmoothie.datasource import Datasource
# import quantipy as qp


def test_incorrect_token():
    client = Client(api_key='incorrect')
    resp = client.get_request('datasource')
    assert resp['detail'] == 'Invalid token.'


def test_new_client(token):
    client = Client(api_key=token)
    resp = client.get_request('datasource')
    assert 'results' in resp


def test_list_datasources(token):
    client = Client(api_key=token)
    resp = client.list_datasources()
    assert 'results' in resp


def test_get_datasource(token):
    client = Client(api_key=token)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    resp = client.get_datasource(primary_key)
    assert isinstance(resp, Datasource)


def test_update_datasource(token, dataset_meta, dataset_data):
    client = Client(api_key=token)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    meta = dataset_meta
    data = dataset_data.to_csv()
    resp = datasource.update_meta_and_data(meta=meta, data=data)
    assert resp.status_code == 200
