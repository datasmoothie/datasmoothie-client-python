

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

    def update_content(self, new_elements):
        """Update report elements with new element list.

        Parameters
        ----------
        new_elements : json
            A json object which has an array of well formed elements.

        Returns
        -------
        type
            Meta data of the updated report.

        """
        return self._client.put_request('reportElement/{}'.format(self._pk),
                                        data=new_elements
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
