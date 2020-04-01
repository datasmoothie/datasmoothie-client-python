

class Report():
    """Represents a report object in datasource.

    Parameters
    ----------
    client : datasource.Client
        The client used to create or fetch the report.
    title : string
        The title of the report.
    primary_key : string
        Primary key of the report in Datasmoothie.

    Attributes
    ----------
    _client : datasmoothie.Client
    _title : string
    _pk : string

    """

    def __init__(self, client, title, elements, primary_key=None):
        self._client = client
        self._title = title
        self._elements = elements
        self._pk = primary_key

    def get_content(self):
        """Get the content of a report, i.e. a list of its elements.

        The returned object is the list of elements in a report, i.e.
        charts, text items and so on.

        Returns
        -------
        type
            List of elements in the report.

        """
        return self._client.get_request('reportElement/{}'.format(self._pk))


    def get_report_meta(self, primary_key):
        result = self._client.get_request('report/{}'.format(primary_key))
        return result

    def get_report_elements(self, primary_key):
        result = self._client.get_request('reportElement/{}'.format(primary_key))
        return result

    def update_content(self, new_content):
        return self._client.put_request('reportElement/{}'.format(self._pk),
                                        data=new_content
                                        )

    def delete(self):
        """Delete this report from Datasmoothie (be careful!).

        Returns
        -------
        type
            The response from the API.

        """
        return self._client.delete_request(resource='report',
                                           primary_key=self._pk)
