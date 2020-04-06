import json
import pandas as pd

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

    def deserialize_dataframe(self, data, index, columns):
        """ Deserializes a dataframe that was serialized with orient='split'
        """
        return pd.DataFrame(data=data,
                            index=pd.MultiIndex.from_tuples(index),
                            columns=pd.MultiIndex.from_tuples(columns)
        )

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

    def get_tables(self, stub, banner, views):
        """ Calculates views for a stub/banner combination

        Parameters
        ----------
        stub : list
            List of variables on the x axis
        banner : list
            List of variables on the y axis
        views : list
            List of view's to calculate
            Unsupported view's are ignored.

        Returns
        -------
        dict
            A dict that contains the views as keys 
            and the results as Pandas DataFrames.
        """
        payload = {
            'stub': stub,
            'banner': banner,
            'views': views
        }
        resp = self._client.post_request(resource='datasource/{}'.format(self._pk),
                                         action="tables/",
                                         data=payload
                                        )
        results = {}
        if resp.status_code == 200:
            content = json.loads(resp.content)
            for view in content['results']:
                results[view] = self.deserialize_dataframe(
                    data=content['results'][view]['data'],
                    index=content['index'],
                    columns=content['results'][view]['columns']
                )
        return results

    def get_table(self, stub, banner, view):
        """ Calculates a single view for a stub/banner combination

        Parameters
        ----------
        stub : list
            List of variables on the x axis
        banner : list
            List of variables on the y axis
        views : string
            A view to calculate

        Returns
        -------
        Pandas.DataFrame OR the response obj
            The resulting Pandas.DataFrame or the response object if it fails
        """
        payload = {
            'stub': stub,
            'banner': banner,
            'view': view
        }
        resp = self._client.post_request(resource='datasource/{}'.format(self._pk),
                                         action="table/",
                                         data=payload
                                        )
        if resp.status_code == 200:
            content = json.loads(resp.content)
            return self.deserialize_dataframe(data=content['data'],
                                              index=content['index'],
                                              columns=content['columns'])
        else:
            return resp

    def get_crosstab(self, stub, banner):
        """ Calculates a single crosstab view for a stub/banner combination

        Parameters
        ----------
        stub : list
            List of variables on the x axis
        banner : list
            List of variables on the y axis
        views : string
            A view to calculate

        Returns
        -------
        Pandas.DataFrame OR the response obj
            The resulting Pandas.DataFrame or the response object if it fails
        """
        payload = {
            'stub': stub,
            'banner': banner
        }
        resp = self._client.post_request(resource='datasource/{}'.format(self._pk),
                                         action="crosstab/",
                                         data=payload
                                        )
        if resp.status_code == 200:
            content = json.loads(resp.content)
            return self.deserialize_dataframe(data=content['data'],
                                              index=content['index'],
                                              columns=content['columns'])
        else:
            return resp
