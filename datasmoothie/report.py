import json
import time
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

from . import templates  # relative-import the *package* containing the templates

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
        """Update the report's meta data.

        Used to update the entire meta data object. Use update_element to
        update just one element.

        Parameters
        ----------
        new_meta : dict
            The meta data that should replace the current meta data.

        Returns
        -------
        type
            Description of returned object.

        """
        payload = new_meta
        if new_meta['global_filter'] == '':
            new_meta['global_filter'] = "default_filter"
        if new_meta['template'] == '':
            new_meta['template'] = "None"
        return self._client.put_request('report/{}'.format(self._pk),
                                        data=payload
                                        )

    def update_meta_element(self, element, new_value):
        """Update a single element in the report's meta data.

        Parameters
        ----------
        element : string
            The name of the element.
        new_value : string
            The new value of the element.


        """
        if element not in self.meta:
            raise ValueError("{} is not in the report meta data.".format(element))
        new_meta = self.meta
        new_meta[element] = new_value
        return self.update_meta(new_meta)

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
        """Get url of the report on datasmoothie.com.

        Returns
        -------
        string
            The link to the report.

        """
        base_url = self._client.get_base_url(api=False)
        return "https://{}{}/{}/".format(base_url,
                                        "@{}".format(self.meta['account']),
                                        self.meta['slug'])

    def add_charts(self,
                  datasource_primary_key,
                  x_y_pairs=[],
                  filters=[],
                  comparison_variables=[],
                  chart_type="StackedBarChart",
                  charts_per_row=1):
        """Add multiple charts to the report.

        Use this method rather than add_chart to add multiple charts at once
        as it is much faster. It adds all the charts to the report and updates
        the server once, whereas add_chart updates the server after each chart.

        Parameters
        ----------
        datasource_primary_key : type
            Description of parameter `datasource_primary_key`.
        x_y_pairs :
            List of tuples, e.g. [('q1', 'gender'), ('q2', 'gender'), ('q3', '@')]
        chart_type : type
            Chart type. Allowed types are StackedBarChart, StackedChartHor.

        Returns
        -------
        type
            Description of returned object.

        """
        for index, variable_pair in enumerate(x_y_pairs):
            # 2 charts per row, this is true on 2, 4, 6, 8 etc.
            same_line_as_previous = (index % charts_per_row > 0 )
            self.add_chart(datasource_primary_key=datasource_primary_key,
                           x=variable_pair[0],
                           y=variable_pair[1],
                           filters=filters,
                           comparison_variables=comparison_variables,
                           chart_type=chart_type,
                           update_server=False,
                           same_line_as_previous=same_line_as_previous)
        self.update_content(self.elements)

    def add_chart(self,
                  datasource_primary_key,
                  x,
                  y="@",
                  title=None,
                  chart_type="StackedBarChart",
                  update_server=True,
                  comparison_variables=[],
                  filters=[],
                  same_line_as_previous=False,
                  language_key=None
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
        update_server : boolean
            Update the server with the new element or just do it locally.
            If it's only local, you need to call self.update_content(new_elements)
            manually.
        same_line_as_previous : boolean
            Should this chart be in the same line as the previous chart, on
            the right? Don't do this for the first chart you add.

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
        datasource = self._client.get_datasource(datasource_primary_key)
        if language_key is None:
            language_key = datasource.get_default_language()
        with pkg_resources.open_text(templates, 'chart.json') as file:
            new_element_json = json.load(file)
        new_element_json['position'] = len(self.elements) + 1
        new_element_json['rowid'] = int(time.time()*1000)
        new_element_json['Type'] = chart_type
        new_element_json['Data']['y'] = y
        new_element_json['Data']['x'] = x
        if same_line_as_previous:
            new_element_json['Data']['hasOnLeft'] = True
        new_element_json['Data']['chartOptions']['filters'] = filters
        new_element_json['Data']['chartOptions']['comparisonvars'] = comparison_variables
        if title is None:
            survey_meta = datasource.get_survey_meta()
            if type(x) != list and x in survey_meta['columns']:
                title_from_meta = survey_meta['columns'][x]['text'][language_key]
                new_element_json['Data']['chartOptions']['title'] = title_from_meta
        else:
            new_element_json['Data']['chartOptions']['title'] = title

        selection = {}
        selection[datasource_primary_key] = {"x": x,
                                             "y": y,
                                             "type": "categorical"
                                             }
        new_element_json['Data']['selectionsByDatasource'] = selection
        new_elements = self.elements
        new_elements.append(new_element_json)
        self.elements = new_elements
        if update_server:
            self.update_content(new_elements)
        return new_element_json
