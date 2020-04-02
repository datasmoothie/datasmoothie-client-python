from datasmoothie import Client
from datasmoothie import Datasource
from datasmoothie import Report
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


def test_list_reports(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    assert 'results' in reports


def test_get_report_meta(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    pk = reports['results'][0]['pk']
    result = client.get_report_meta(pk)
    print(result)
    assert 'pk' in result

def test_get_report(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    pk = reports['results'][0]['pk']
    report = client.get_report(pk)
    print(report.title)
    print(report.elements)
    assert isinstance(report, Report)


def test_create_report(token):
    client = Client(api_key=token)
    number_of_reports = client.list_reports()['count']
    report = client.create_report(title="api created report")
    assert client.list_reports()['count'] == number_of_reports + 1
    report.delete()
    assert client.list_reports()['count'] == number_of_reports
