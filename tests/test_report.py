import json
import time

from datasmoothie import Client
from datasmoothie import Report



def test_get_content(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    reports = client.list_reports()
    report = client.get_report_elements(reports['results'][0]['pk'])
    print(report)
    assert 'elements' in report


def test_get_url(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    reports = client.list_reports()
    report = client.get_report(reports['results'][0]['pk'])
    assert len(report.get_url()) > 0


def test_create_report_and_add_chart(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    datasource_pk = client.list_datasources()['results'][0]['pk']
    report = client.create_report('my test')
    original_length = len(report.elements)
    resp = report.add_chart(datasource_pk,
                            ['numitems', 'org'],
                            y='agecat')
    report2 = client.get_report(report._pk)
    report.delete()
    assert len(report2.elements) == original_length + 1
    assert 'Type' in resp

def test_update_meta_element(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    reports = client.list_reports()
    datasources = client.list_datasources()
    datasource_id = datasources['results'][0]['pk']
    report = client.get_report(reports['results'][0]['pk'])
    meta = report.meta
    resp = report.update_meta_element('title', 'new title')
    assert resp.status_code == 200
    report = client.get_report(reports['results'][0]['pk'])
    assert report.meta['title'] == 'new title'

def test_update_report_meta(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    reports = client.list_reports()
    datasources = client.list_datasources()
    datasource_id = datasources['results'][0]['pk']
    report = client.get_report(reports['results'][0]['pk'])
    meta = report.meta
    meta['title'] = 'changed'
    resp = report.update_meta(meta)
    assert resp.status_code == 200
    report = client.get_report(reports['results'][0]['pk'])
    assert report.meta['title'] == 'changed'

def test_add_chart(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    reports = client.list_reports()
    datasources = client.list_datasources()
    datasource_id = datasources['results'][0]['pk']
    report = client.get_report(reports['results'][0]['pk'])
    original_length = len(report.elements)
    report.add_chart(datasource_primary_key=datasource_id,
                     x=['service', 'quality'])
    report = client.get_report(reports['results'][0]['pk'])
    assert len(report.elements) == original_length + 1

def test_add_multipl_charts(token):
    client = Client(api_key=token, host="localhost:8030/api2", ssl=False)
    reports = client.list_reports()
    datasources = client.list_datasources()
    datasource_id = datasources['results'][0]['pk']
    report = client.get_report(reports['results'][0]['pk'])
    original_length = len(report.elements)
    report.add_charts(datasource_primary_key=datasource_id,
                     x_y_pairs=[('price', 'gender'),
                                ('quality', '@'),
                                ('service', '@'),
                                ('distance', '@'),
                                ('quality', '@'),
                                ('quality', '@'),
                                ('quality', '@'),
                                ('quality', '@')],
                     filters=['gender', 'agecat'],
                     comparison_variables=['agecat'],
                     charts_per_row=3)
    report = client.get_report(report._pk)
    assert len(report.elements) == original_length + 8
