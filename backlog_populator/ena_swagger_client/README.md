# swagger-client
No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 1.2
- Package version: 1.0.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import swagger_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import swagger_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
swagger_client.configuration.username = 'YOUR_USERNAME'
swagger_client.configuration.password = 'YOUR_PASSWORD'
# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
result = 'result_example' # str | The result type (data set) to search against. Is mandatory.
query = 'query_example' # str | A set of search conditions joined by logical operators (AND, OR, NOT) and bound by double quotes. If none supplied, the full result set will be returned. (optional)
data_portal = 'data_portal_example' # str | The data portal ID. Defaults to 'ena'. (optional)
dcc_data_only = true # bool | Whether to limit the search to only DCC records. By default, all public data is also included in the search. (optional)
include_metagenomes = true # bool | Whether to include public metagenome data in the search. By default, these are not included. Note that any metagenome data associated with a DCC hub will always be included in a search against that DCC. (optional)

try:
    # Count rows matching search parameters
    api_response = api_instance.count_using_get(result, query=query, data_portal=data_portal, dcc_data_only=dcc_data_only, include_metagenomes=include_metagenomes)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->count_using_get: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://www.ebi.ac.uk/ena/portal/api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*PortalAPIApi* | [**count_using_get**](docs/PortalAPIApi.md#count_using_get) | **GET** /count | Count rows matching search parameters
*PortalAPIApi* | [**do_sample_links_using_get**](docs/PortalAPIApi.md#do_sample_links_using_get) | **GET** /links/sample | Sample links
*PortalAPIApi* | [**do_study_links_using_get**](docs/PortalAPIApi.md#do_study_links_using_get) | **GET** /links/study | Study links
*PortalAPIApi* | [**do_taxon_links_using_get**](docs/PortalAPIApi.md#do_taxon_links_using_get) | **GET** /links/taxon | Taxonomy links
*PortalAPIApi* | [**download_doc_using_get**](docs/PortalAPIApi.md#download_doc_using_get) | **GET** /doc | Download the documentation as a PDF file.
*PortalAPIApi* | [**file_report_using_get**](docs/PortalAPIApi.md#file_report_using_get) | **GET** /filereport | Get file report from warehouse search
*PortalAPIApi* | [**get_controlled_vocab_using_get**](docs/PortalAPIApi.md#get_controlled_vocab_using_get) | **GET** /controlledVocab | Get a list of available values for a controlled vocabulary field.
*PortalAPIApi* | [**get_results_using_get**](docs/PortalAPIApi.md#get_results_using_get) | **GET** /results | Get a list of available result types (data sets) to search against.
*PortalAPIApi* | [**get_return_fields_using_get**](docs/PortalAPIApi.md#get_return_fields_using_get) | **GET** /returnFields | Get a list of fields that can be returned for a result type.
*PortalAPIApi* | [**get_search_fields_using_get**](docs/PortalAPIApi.md#get_search_fields_using_get) | **GET** /searchFields | Get a list of searchable fields for a result type.
*PortalAPIApi* | [**search_post_using_post**](docs/PortalAPIApi.md#search_post_using_post) | **POST** /search | Perform a warehouse search with POST
*PortalAPIApi* | [**search_using_get**](docs/PortalAPIApi.md#search_using_get) | **GET** /search | Perform a warehouse search


## Documentation For Models



## Documentation For Authorization


## basicAuth

- **Type**: HTTP basic authentication


## Author


