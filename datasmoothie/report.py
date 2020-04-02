import json
import time

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

    def __init__(self, client, meta, elements, primary_key=None):
        self._client = client
        self._pk = primary_key
        self.title = meta['title']
        self.meta = meta
        self.elements = elements

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

    def update_meta(self, new_meta):
        payload = new_meta
        return self._client.put_request('report/{}'.format(self._pk),
                                        data=payload
                                        )

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
        payload = {"elements":new_elements}
        return self._client.put_request('reportElement/{}'.format(self._pk),
                                        data=payload
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

    def get_url(self):
        base_url = self._client.get_base_url(api=False)
        return "https://{}{}/{}/".format(base_url,
                                        "@{}".format(self.meta['account']),
                                        self.meta['slug'])

    def add_chart(self,
                  datasource_primary_key,
                  x,
                  y="@",
                  chart_type="StackedBarChart",
                  ):
        """Add a chart to the report.

        Add a chart to the report. The chart will be the
        last element in the report. The user supplies information
        on what datasource the chart should come from and what
        the names of the variables are. If incorrect names are used
        the chart is still added but it won't work in the dashboard.

        Parameters
        ----------
        datasource_primary_key : type
            Primary key of the datasource used for the chart.
        x : string or array of strings
            The "top" variable for the chart.
        y : string
            A variable to use as a crosstab for the chart,
            e.g. 'age_groups'.
        chart_type : string
            Chart type to use.

        Returns
        -------
        type
            JSON object representing the new element.

        """
        if x is None:
            raise ValueError("x must be a valid variable")
        if datasource_primary_key is None:
            raise ValueError("datasource primary key must be defined")
        if self.meta['datasource'] is None:
            datasource_url = "https://{}/datasource/{}/".format(self._client.get_base_url(),
                                                                 datasource_primary_key)
            self.meta['datasource'] = datasource_url
        new_meta = self.meta
        self.update_meta(new_meta)
        new_element_json = {}
        with open('datasmoothie/templates/chart.json') as file:
            new_element_json = json.load(file)
        new_element_json['position'] = len(self.elements) + 1
        new_element_json['rowid'] = int(time.time()*1000)
        new_element_json['Type'] = chart_type
        new_element_json['Data']['y'] = y
        new_element_json['Data']['x'] = x
        selection = {}
        selection[datasource_primary_key] = {"x": x,
                                             "y": y,
                                             "type": "categorical"
                                             }
        new_element_json['Data']['selectionsByDatasource'] = selection
        new_elements = self.elements
        new_elements.append(new_element_json)
        self.update_content(new_elements)
        return new_element_json
