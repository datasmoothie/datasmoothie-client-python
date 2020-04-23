import json
import os.path

from datasmoothie import Client
from datasmoothie import Report
from datasmoothie import Datasource

def test_get_meta_and_data(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    resp = datasource.get_meta_and_data()
    print(resp.keys())
    assert 'meta' in resp
    assert 'data' in resp

def test_get_tables(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    tables = datasource.get_tables(['price', 'quality'],
                                   ['gender', 'agecat'],
                                   ['cbase', 'counts', 'c%', 'stddev'],
                                   combine=True,
                                   language='en-GB')
    assert tables['counts'].shape == (10, 7)
    assert tables['c%'].shape == (10, 7)
    assert tables['stddev'].shape == (2, 7)
    assert tables['cbase'].shape == (2,7)
    assert False

def test_get_tables(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    tables = datasource.get_tables(['price', 'quality'],
                                   ['gender', 'agecat'],
                                   ['cbase', 'counts', 'c%', 'stddev'],
                                   combine=False,
                                   language='en-GB')
    assert tables['counts'].shape == (10, 7)
    assert tables['c%'].shape == (10, 7)
    assert tables['stddev'].shape == (2, 7)
    assert tables['cbase'].shape == (2,7)

def test_get_combined_tables(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    tables = datasource.get_tables(['price', 'quality'],
                                   ['gender', 'agecat'],
                                   ['counts', 'c%', 'cbase', 'stddev'],
                                   combine=True,
                                   language='en-GB')
    assert tables.shape == (24,7)

def test_get_table_set(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    stubs = [
                ['distance', 'store', 'contact'],
                ['reason1', 'reason2', 'dept'],
                ['price', 'numitems', 'org', 'service', 'quality', 'overall']
              ]
    banners = [['gender', 'agecat'], ['regular', 'purchase']]
    table_set = datasource.get_table_set(stubs, banners, ['base', 'counts', 'c%', 'stddev'])
    assert len(table_set) == len(stubs) * len(banners)

def test_dataset_to_excel(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    datasources = client.list_datasources()
    primary_key = datasources['results'][0]['pk']
    datasource = client.get_datasource(primary_key)
    stubs = [
                ['distance', 'store', 'contact'],
                ['reason1', 'reason2', 'dept'],
                ['price', 'numitems', 'org', 'service', 'quality', 'overall']
              ]
    banners = [['gender', 'agecat'], ['regular', 'purchase']]
    table_set = datasource.get_table_set(stubs, banners, ['base', 'counts', 'c%', 'stddev'])
    datasource.table_set_to_excel(table_set, 'myexcel.xlsx')
    assert os.path.isfile('myexcel.xlsx')
    os.remove("myexcel.xlsx")
