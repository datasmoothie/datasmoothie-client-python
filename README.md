# Python wrapper for Datasmoothie

## Introduction
This is the python wrapper for the Datasmoothie API. Datasmoothie is a platform that helps people with data processing and visualisation of survey data, weighting and recoding to visualising in interactive dashboards.

The Datasmoothie API is organised around REST. The API has resource oriented URLs, accepts form-encoded requests, returns JSON-encoded responses and uses standard HTTP response codes, authentication and verbs.

### Install and import
Install the client library via the command line:

```pip install --upgrade datasmoothie```

We recommend importing datasmoothie and preserving the namespace:

```import datasmoothie```

## Authenticate
The Datasmoothie API uses API keys to authenticate requests. Datasmoothie users each have their own API key automatically associated with them.

Your API key grants you many privileges, make sure to keep it safe! Don’t check it into a code repository or share it with anyone. Each user should have their own API so that permissions can be revoked if necessary.

To use your API key:

```
import datasmoothie
client = datasmoothie.client(api_key = "[your_key]")
```
The client object can then be used to easily interface with the API.

### Example usage

```
datasource = client.get_datasource(id)
datasource.update_meta_and_data(meta=json_file, data=csv_file)

```
