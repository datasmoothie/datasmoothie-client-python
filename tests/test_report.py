from datasmoothie import Client
from datasmoothie import Report



def test_get_content(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    report = client.get_report_elements(reports['results'][0]['pk'])
    print(report)
    assert 'elements' in report


def test_update_content(token):
    client = Client(api_key=token)
    reports = client.list_reports()
    report = client.get_report_elements(reports['results'][0]['pk'])
    assert 'elements' in report
