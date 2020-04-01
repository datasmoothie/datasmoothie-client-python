import json
import requests
from .datasource import Datasource
from .report import Report

HOST = "www.datasmoothie.com/api2"


class Client:
    """Client that makes first calls to the Datasmoothie API.

    Parameters
    ----------
    api_key : string
        API key used to authenticate calls. This is provided by Datasmoothie.

    Attributes
    ----------
    __api_key : string
        The API key used for authentication.
    __headers : type
        The headers used for http requests.

    """

    def __init__(self, api_key):
        """Initialise the client with an API key.

        Parameters
        ----------
        api_key : string
            The API key used for authentication, provided by Datasmoothie.


        """
        self.__api_key = api_key
        self.__headers = {
            "Authorization": "Token {}".format(self.__api_key),
            "content-type": "application/json"
            }

    def _get_headers(self):
        return self.__headers

    def get_request(self, resource, action=None):
        """Send a get request to the API with a convenient wrapper.

        Parameters
        ----------
        resource : string
            Name of the resource we are calling.
            These are the root paths of the API.
        action : type
            Name of the action to take on the resouce,
            e.g. datasource/1/meta_data

        Returns
        -------
        type
            JSON object representing the result of the API request.

        """
        base_url = "https://{}".format(HOST)
        if action is None:
            action = ""
        request_path = "{}/{}/{}".format(base_url, resource, action)
        result = requests.get(request_path, headers=self._get_headers())
        result = json.loads(result.content)
        return result

    def post_request(self, resource, action="", data={}):
        """Send a POST request to the API with a wrapper.

        This is used by other objects
        to call the API and not used by the users themselves.

        Parameters
        ----------
        resource : string
            Name of the resource we are calling.
            These are the root paths of the API.
        action : type
            Name of the action to take on the resouce,
            e.g. datasource/1/meta_data
        data : type
            JSON object with the payload to send with a POST request.

        Returns
        -------
        type
            Description of returned object.

        """
        base_url = "https://{}".format(HOST)
        request_path = "{}/{}/{}".format(base_url, resource, action)
        result = requests.post(request_path,
                               headers=self._get_headers(),
                               data=json.dumps(data)
                               )
        return result

    def put_request(self, resource, data):
        base_url = "https://{}".format(HOST)
        request_path = "{}/{}".format(base_url, resource)
        result = requests.put(request_path,
                              headers=self._get_headers(),
                              json=json.dumps(data)
                              )
        return result

    def delete_request(self, resource, primary_key):
        """Send a delete request to the API.

        Parameters
        ----------
        resource : string
            Path location of the resource.
        primary_key : string
            The reports primary key, as reported by get reports.

        Returns
        -------
        type
            The response from the server.

        """
        base_url = "https://{}".format(HOST)
        request_path = "{}/{}/{}".format(base_url, resource, primary_key)
        result = requests.delete(request_path,
                                 headers=self._get_headers())
        return result

    def get_datasource(self, primary_key):
        """Create a datasource object from information fetched from the API.

        Parameters
        ----------
        primaryKey : integer
            The primary key of the datasource.

        Returns
        -------
        type
            A Datasource object.

        """
        result = self.get_request('datasource/{}'.format(primary_key))
        datasource = Datasource(client=self,
                                name=result['name'],
                                primary_key=result['pk'])
        return datasource

    def list_datasources(self):
        """Get a list of all the datasources this account has.

        Returns
        -------
        type
            A JSON object with meta information about the datasources.
            This can be used to get the primary keys of the datasource
            the user wants to manipulate.

        """
        result = self.get_request('datasource')
        return result

    def create_report(self, title):
        resp = self.post_request('report', data={"title": title})
        resp = json.loads(resp.content)
        report = Report(client=self,
                        title=resp['title'],
                        primary_key=resp['pk'],
                        elements=[]
                        )
        return report

    def list_reports(self):
        """Get a list of all reports this account has.

        Returns
        -------
        type
            List of reports in json form.

        """
        result = self.get_request('report')
        return result

    def get_report_meta(self, primary_key):
        result = self.get_request('report/{}'.format(primary_key))
        return result

    def get_report_elements(self, primary_key):
        result = self.get_request('reportElement/{}'.format(primary_key))
        return result

    def get_report(self, primary_key):
        meta = self.get_report_meta(primary_key)
        elements = self.get_report_elements(primary_key)
        report = Report(self, meta['title'], elements['elements'], primary_key)
        return report
