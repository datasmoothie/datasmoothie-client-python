

class Datasource:
    """A class that represents a Datasmoothie datasource.

    This is used
    to make it easy to upload data, update data and do any operation
    the user needs to do on a dataset.

    Parameters
    ----------
    client : datasmoothie.Client
        The client that will interface with the API.
    name : string
        Name of the Datasource.
    primaryKey : integer
        The identifier for the datasource.

    Attributes
    ----------
    _name : string
        Name of the datasource.
    _client : datasmoothie.Client
        The client that will interface with the API.
    _pk : integer
        Identifier of the datasource in Datasmoothie.

    """

    def __init__(self, client, meta, primary_key):
        """Initialise a Datasource.

        Parameters
        ----------
        client : A Datasmoothie python client.
            A Datasmothie python client that has a valid api token.
        name : string
            Datasource name.
        primaryKey : type
            The primary key of the Datasource in Datasmoothie.


        """
        self.survey_meta = {}
        self.survey_data = ""
        self.meta = meta
        self.name = meta['name']
        self._client = client
        self._pk = primary_key

    def name(self):
        """Get name of datasource.

        Returns
        -------
        type
            Datasource name.

        """
        return self._name

    def get_meta_and_data(self):
        """Get meta data and data for a data source.

        Returns
        -------
        json dict
            Returns a dict with two keys, meta and data. The meta is
            Quantipy meta data and the data is a csv with the response data.

        """
        resp = self._client.get_request('datasource/{}'.format(self._pk),
                                        'meta_data')
        self.survey_meta = resp['meta']
        self.survey_data = resp['data']
        return resp

    def update_meta_and_data(self, meta, data):
        """Update the remote datasource with new meta-data and data.

        Parameters
        ----------
        meta : json object
            Meta data (in quantipy form).
        data : string
            A CSV file with the dataset's data.

        Returns
        -------
        type
            The Json object the API returned.
        """
        payload = {
            'meta': meta,
            'data': data
        }
        resp = self._client.post_request('datasource/{}'.format(self._pk),
                                         'meta_data',
                                         data=payload
                                         )
        return resp
