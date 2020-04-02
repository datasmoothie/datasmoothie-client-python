import json
import time

from datasmoothie import Client
from datasmoothie import Report



def test_get_content(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    report = client.get_report_elements(reports['results'][0]['pk'])
    print(report)
    assert 'elements' in report


def test_get_url(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    report = client.get_report(reports['results'][0]['pk'])
    assert "datasmoothie.com" in report.get_url()


def test_create_report_and_add_chart(token):
    client = Client(api_key=token)
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

def test_add_chart(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    datasources = client.list_datasources()
    datasource_id = datasources['results'][0]['pk']
    report = client.get_report(reports['results'][0]['pk'])
    original_length = len(report.elements)
    report.add_chart(datasource_primary_key=datasource_id,
                     x=['service', 'quality'])
    report = client.get_report(reports['results'][0]['pk'])
    assert len(report.elements) == original_length + 1
