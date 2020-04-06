import json
import requests
from .datasource import Datasource
from .report import Report


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

    def __init__(self, api_key, host="www.datasmoothie.com/api2", ssl=True):
        """Initialise the client with an API key.

        Parameters
        ----------
        api_key : string
            The API key used for authentication, provided by Datasmoothie.
        host : string
            The path to the server api
        ssl : boolean
            Datasmoothie does not support non ssl communication, but this is 
            useful for development and local unit testing.

        """
        self.host = host
        if ssl:
            self.base_url = "https://{}".format(host)
        else:
            self.base_url = "http://{}".format(host)
        self.__api_key = api_key
        self.__headers = {
            "Authorization": "Token {}".format(self.__api_key),
            "Content-Type": "application/json",
            "Accept": "application/json"
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
        if action is None:
            action = ""
        request_path = "{}/{}/{}".format(self.base_url, resource, action)
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
        
        request_path = "{}/{}/{}".format(self.base_url, resource, action)
        result = requests.post(request_path,
                               headers=self._get_headers(),
                               data=json.dumps(data)
                               )
        return result

    def put_request(self, resource, data):
        request_path = "{}/{}/".format(self.base_url, resource)
        result = requests.put(request_path,
                              headers=self._get_headers(),
                              json=data
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
        request_path = "{}/{}/{}".format(self.base_url, resource, primary_key)
        result = requests.delete(request_path,
                                 headers=self._get_headers())
        return result

    def get_base_url(self, api=True):
        if api:
            return self.host
        else:
            return self.host.replace("api2", "")

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
                                meta=result,
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

    def create_report(self, title, global_filter="default", template="none"):
        """Create a report/dashboard in Datasmoothie.

        Parameters
        ----------
        title : string
            Repor title. This will be displayed at the top of the report.

        Returns
        -------
        type
            The created report with both meta and content (elements).

        """
        resp = self.post_request('report',
                                 data={"title": title,
                                       "global_filter": global_filter,
                                       "template": template})
        resp = json.loads(resp.content)
        report = Report(client=self,
                        meta=resp,
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
        """Met meta data for the report.

        This includes the title, subtitle, slug and so on but doesn't
        include the contents themselves. Get thos with get_report_elements.

        Parameters
        ----------
        primary_key : int

        Returns
        -------
        type
            Returns json object with all the meta data of the report.

        """
        result = self.get_request('report/{}'.format(primary_key))
        return result

    def get_report_elements(self, primary_key):
        """Get the elements of the report (the content).

        The elements are the charts, text, images and so on of the report.

        Parameters
        ----------
        primary_key : int

        Returns
        -------
        type
            A json object which is an array with all the elements.

        """
        result = self.get_request('reportElement/{}'.format(primary_key))
        return result

    def get_report(self, primary_key):
        """Get datasmoothie report.

        This creates a wrapper Report object and fetches both the
        meta data and the elements array (content).

        Parameters
        ----------
        primary_key : type

        Returns
        -------
        type
            Datasmoothie Report object.

        """
        meta = self.get_report_meta(primary_key)
        elements = self.get_report_elements(primary_key)
        report = Report(self, meta, elements['elements'], primary_key)
        return report
