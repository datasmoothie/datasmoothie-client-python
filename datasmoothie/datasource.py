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

    def get_tables(self, stub, banner, views, combine=False, language=None):
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
                                         action="tables",
                                         data=payload
                                        )
        results = {}
        if resp.status_code == 200:
            content = json.loads(resp.content)
            for view in content['results']:
                results[view] = self.deserialize_dataframe(
                    data=content['results'][view]['data'],
                    index=content['results'][view]['index'],
                    columns=content['results'][view]['columns']
                )
        #remove invalide views
        views = [i for i in views if i in results.keys()]
        if 'counts' in views:
            results['counts'] = results['counts'].astype(int)
        if 'c%' in views:
            results['c%'] = results['c%'].round(1)

        # to combine % and counts, we merge them row by row
        if 'c%' in views and 'counts' in views and combine:
            mi_pct = results['c%'].index
            mi_counts = results['counts'].index
            values = results['c%'].index.levels[1]
            mi_pct = mi_pct.set_levels(level=1,
                                   levels=["{} (%)".format(i) for i in values])
            mi_counts = mi_counts.set_levels(level=1,
                                   levels=["{}".format(i) for i in values])
            results['c%'].index = mi_pct
            results['counts'].index = mi_counts
            results['c%'] = pd.concat([results['counts'], results['c%']]).sort_index(level=0)
            del results['counts']
            views.remove('counts')
        if combine and len(views) > 1:
            combined = results[views[0]]
            for view in views[1:]:
                combined = pd.concat([combined, results[view]])
            combined.index = self.apply_labels(combined.index)
            combined.columns = self.apply_labels(combined.columns)
            return combined
        else:
            return results

    def get_table_set(self, stubs, banners, views, language=None):
        table_set = []
        for stub in stubs:
            for banner in banners:
                table = self.get_tables(stub,
                                        banner,
                                        views,
                                        combine=True,
                                        language=language)
                table_set.append(table)
        return table_set

    def table_set_to_excel(self, table_set, filename):
        writer = pd.ExcelWriter('{}'.format(filename), engine="xlsxwriter")
        workbook = writer.book
        left_format = workbook.add_format({'align':'left'})
        left_format.set_align('left')
        for index, table in enumerate(table_set):
            table.to_excel(writer,
                        startrow=2,
                        sheet_name="Table {}".format(index))

            datasheet = writer.sheets["Table {}".format(index)]
            datasheet.set_column(0,0,20, left_format)
            datasheet.set_column(1,1,20, left_format)

        writer.save()

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

    def get_survey_meta(self):
        if self.survey_meta == {}:
            resp = self.get_meta_and_data()
            return resp['meta']
        else:
            return self.survey_meta

    def apply_labels(self, index, text_key=None):
        if text_key is None:
            text_key = self.get_survey_meta()['lib']['default text']
        tuple_list = index.to_native_types()
        new_list = []
        for t in tuple_list:
            code = t[1]
            variable = t[0]
            value_map = self.get_values(variable)
            try:
                code = int(code)
            except Exception as e:
                pass
            if code in value_map.keys():
                value = value_map[code]
            else:
                if '%' in code:
                    value = '%'
                else:
                    value = code
            variable = self.text(variable)
            new_list.append((variable, value))
        return pd.MultiIndex.from_tuples(new_list, names=["Questions", "Values"])


    def text(self, name, text_key=None):
        """
        Return the variables text label information.

        Parameters
        ----------
        name : str, default None
            The variable name keyed in ``_meta['columns']``.
        text_key : str, default None
            The default text key to be set into the new meta document.

        Returns
        -------
        text : str
            The text metadata.
        """
        if text_key is None: text_key = self.get_survey_meta()['lib']['default text']
        return self.get_survey_meta()['columns'][name]['text'].get(text_key, '')

    def get_values(self, variable, text_key=None):
        if text_key is None:
            text_key = self.get_survey_meta()['lib']['default text']
        mapper = {}
        for i in self.get_survey_meta()['columns'][variable]['values']:
            mapper[i['value']] = i['text'][text_key]
        return mapper
