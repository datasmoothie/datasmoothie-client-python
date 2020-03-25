# from .client import Client


class Datasource:

    def __init__(self, client, name, primaryKey):
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
        self._name = name
        self._client = client
        self._pk = primaryKey

    def name(self):
        """Get name of datasource.

        Returns
        -------
        type
            Datasource name.

        """
        return self._name

    def update(self, dataset):
        """Update the remote datasource with new meta-data and data.

        Parameters
        ----------
        dataset : quantipy.Dataset
            A Quantipy Dataset object.

        """
        payload = {
            'meta': dataset.meta(),
            'data': dataset.data()
        }
        self._client.post_request('datasource/{}'.format(self._pk),
                                  'meta_data',
                                  data=payload
                                  )
