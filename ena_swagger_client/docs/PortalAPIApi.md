# swagger_client.PortalAPIApi

All URIs are relative to *https://www.ebi.ac.uk/ena/portal/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**count_using_get**](PortalAPIApi.md#count_using_get) | **GET** /count | Count rows matching search parameters
[**do_sample_links_using_get**](PortalAPIApi.md#do_sample_links_using_get) | **GET** /links/sample | Sample links
[**do_study_links_using_get**](PortalAPIApi.md#do_study_links_using_get) | **GET** /links/study | Study links
[**do_taxon_links_using_get**](PortalAPIApi.md#do_taxon_links_using_get) | **GET** /links/taxon | Taxonomy links
[**download_doc_using_get**](PortalAPIApi.md#download_doc_using_get) | **GET** /doc | Download the documentation as a PDF file.
[**file_report_using_get**](PortalAPIApi.md#file_report_using_get) | **GET** /filereport | Get file report from warehouse search
[**get_controlled_vocab_using_get**](PortalAPIApi.md#get_controlled_vocab_using_get) | **GET** /controlledVocab | Get a list of available values for a controlled vocabulary field.
[**get_results_using_get**](PortalAPIApi.md#get_results_using_get) | **GET** /results | Get a list of available result types (data sets) to search against.
[**get_return_fields_using_get**](PortalAPIApi.md#get_return_fields_using_get) | **GET** /returnFields | Get a list of fields that can be returned for a result type.
[**get_search_fields_using_get**](PortalAPIApi.md#get_search_fields_using_get) | **GET** /searchFields | Get a list of searchable fields for a result type.
[**search_post_using_post**](PortalAPIApi.md#search_post_using_post) | **POST** /search | Perform a warehouse search with POST
[**search_using_get**](PortalAPIApi.md#search_using_get) | **GET** /search | Perform a warehouse search


# **count_using_get**
> str count_using_get(result, query=query, data_portal=data_portal, dcc_data_only=dcc_data_only, include_metagenomes=include_metagenomes)

Count rows matching search parameters

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi(swagger_client.ApiClient(configuration))
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

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result** | **str**| The result type (data set) to search against. Is mandatory. | 
 **query** | **str**| A set of search conditions joined by logical operators (AND, OR, NOT) and bound by double quotes. If none supplied, the full result set will be returned. | [optional] 
 **data_portal** | **str**| The data portal ID. Defaults to &#39;ena&#39;. | [optional] 
 **dcc_data_only** | **bool**| Whether to limit the search to only DCC records. By default, all public data is also included in the search. | [optional] 
 **include_metagenomes** | **bool**| Whether to include public metagenome data in the search. By default, these are not included. Note that any metagenome data associated with a DCC hub will always be included in a search against that DCC. | [optional] 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: text/plain, application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **do_sample_links_using_get**
> str do_sample_links_using_get(accession=accession, result=result, offset=offset, limit=limit, format=format)

Sample links

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
accession = 'accession_example' # str | Sample accession (optional)
result = 'result_example' # str | The result type of links. (optional)
offset = 56 # int | How many records to skip from the beginning in the results. Default value is 0. (optional)
limit = 56 # int | The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. (optional)
format = 'format_example' # str | What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. (optional)

try:
    # Sample links
    api_response = api_instance.do_sample_links_using_get(accession=accession, result=result, offset=offset, limit=limit, format=format)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->do_sample_links_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **accession** | **str**| Sample accession | [optional] 
 **result** | **str**| The result type of links. | [optional] 
 **offset** | **int**| How many records to skip from the beginning in the results. Default value is 0. | [optional] 
 **limit** | **int**| The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. | [optional] 
 **format** | **str**| What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **do_study_links_using_get**
> str do_study_links_using_get(accession=accession, result=result, offset=offset, limit=limit, format=format)

Study links

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
accession = 'accession_example' # str | Sample accession (optional)
result = 'result_example' # str | The result type of links. (optional)
offset = 56 # int | How many records to skip from the beginning in the results. Default value is 0. (optional)
limit = 56 # int | The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. (optional)
format = 'format_example' # str | What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. (optional)

try:
    # Study links
    api_response = api_instance.do_study_links_using_get(accession=accession, result=result, offset=offset, limit=limit, format=format)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->do_study_links_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **accession** | **str**| Sample accession | [optional] 
 **result** | **str**| The result type of links. | [optional] 
 **offset** | **int**| How many records to skip from the beginning in the results. Default value is 0. | [optional] 
 **limit** | **int**| The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. | [optional] 
 **format** | **str**| What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **do_taxon_links_using_get**
> str do_taxon_links_using_get(accession=accession, result=result, offset=offset, limit=limit, subtree=subtree, format=format)

Taxonomy links

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
accession = 'accession_example' # str | Taxon Id (optional)
result = 'result_example' # str | The result type of links. (optional)
offset = 56 # int | How many records to skip from the beginning in the results. Default value is 0. (optional)
limit = 56 # int | The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. (optional)
subtree = true # bool | Inlcude Subtree (optional)
format = 'format_example' # str | What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. (optional)

try:
    # Taxonomy links
    api_response = api_instance.do_taxon_links_using_get(accession=accession, result=result, offset=offset, limit=limit, subtree=subtree, format=format)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->do_taxon_links_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **accession** | **str**| Taxon Id | [optional] 
 **result** | **str**| The result type of links. | [optional] 
 **offset** | **int**| How many records to skip from the beginning in the results. Default value is 0. | [optional] 
 **limit** | **int**| The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. | [optional] 
 **subtree** | **bool**| Inlcude Subtree | [optional] 
 **format** | **str**| What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_doc_using_get**
> str download_doc_using_get()

Download the documentation as a PDF file.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()

try:
    # Download the documentation as a PDF file.
    api_response = api_instance.download_doc_using_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->download_doc_using_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **file_report_using_get**
> str file_report_using_get(result, accession, fields=fields, offset=offset, limit=limit, format=format, download=download)

Get file report from warehouse search

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi(swagger_client.ApiClient(configuration))
result = 'result_example' # str | The result type (data set) to search against. Is mandatory.
accession = 'accession_example' # str | Accession
fields = 'fields_example' # str | A list of fields (comma separated) to be returned in the result. If none supplied, the accession and ftp information for fastq,submitted and sra files will be returned. (optional)
offset = 56 # int | How many records to skip from the beginning in the results. Default value is 0. (optional)
limit = 56 # int | The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. (optional)
format = 'format_example' # str | What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. (optional)
download = true # bool | Whether to download the result as a file, rather than read it from the stream. By default, this is false. (optional)

try:
    # Get file report from warehouse search
    api_response = api_instance.file_report_using_get(result, accession, fields=fields, offset=offset, limit=limit, format=format, download=download)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->file_report_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result** | **str**| The result type (data set) to search against. Is mandatory. | 
 **accession** | **str**| Accession | 
 **fields** | **str**| A list of fields (comma separated) to be returned in the result. If none supplied, the accession and ftp information for fastq,submitted and sra files will be returned. | [optional] 
 **offset** | **int**| How many records to skip from the beginning in the results. Default value is 0. | [optional] 
 **limit** | **int**| The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. | [optional] 
 **format** | **str**| What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. | [optional] 
 **download** | **bool**| Whether to download the result as a file, rather than read it from the stream. By default, this is false. | [optional] 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: text/plain, application/json
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_controlled_vocab_using_get**
> str get_controlled_vocab_using_get(field)

Get a list of available values for a controlled vocabulary field.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
field = 'field_example' # str | Field name

try:
    # Get a list of available values for a controlled vocabulary field.
    api_response = api_instance.get_controlled_vocab_using_get(field)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->get_controlled_vocab_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **field** | **str**| Field name | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_results_using_get**
> str get_results_using_get(data_portal)

Get a list of available result types (data sets) to search against.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
data_portal = 'data_portal_example' # str | Data portal Id

try:
    # Get a list of available result types (data sets) to search against.
    api_response = api_instance.get_results_using_get(data_portal)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->get_results_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_portal** | **str**| Data portal Id | 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_return_fields_using_get**
> str get_return_fields_using_get(result, data_portal=data_portal)

Get a list of fields that can be returned for a result type.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
result = 'result_example' # str | Result
data_portal = 'data_portal_example' # str | Data portal Id (optional)

try:
    # Get a list of fields that can be returned for a result type.
    api_response = api_instance.get_return_fields_using_get(result, data_portal=data_portal)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->get_return_fields_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result** | **str**| Result | 
 **data_portal** | **str**| Data portal Id | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_search_fields_using_get**
> str get_search_fields_using_get(result, data_portal=data_portal)

Get a list of searchable fields for a result type.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi()
result = 'result_example' # str | Result
data_portal = 'data_portal_example' # str | Data portal Id (optional)

try:
    # Get a list of searchable fields for a result type.
    api_response = api_instance.get_search_fields_using_get(result, data_portal=data_portal)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->get_search_fields_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result** | **str**| Result | 
 **data_portal** | **str**| Data portal Id | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_post_using_post**
> str search_post_using_post(result, query=query, fields=fields, sort_fields=sort_fields, offset=offset, limit=limit, data_portal=data_portal, dcc_data_only=dcc_data_only, include_metagenomes=include_metagenomes, email=email, saved_search=saved_search, format=format, download=download)

Perform a warehouse search with POST

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi(swagger_client.ApiClient(configuration))
result = 'result_example' # str | The result type (data set) to search against. Is mandatory.
query = 'query_example' # str | A set of search conditions joined by logical operators (AND, OR, NOT) and bound by double quotes. If none supplied, the full result set will be returned. (optional)
fields = 'fields_example' # str | A list of fields (comma separated) to be returned in the result. If none supplied, the accession and description/title of the main result object will be returned. (optional)
sort_fields = 'sort_fields_example' # str | A list of fields (comma separated) in the order of which the results should be sorted. (optional)
offset = 56 # int | How many records to skip from the beginning in the results. Default value is 0. (optional)
limit = 56 # int | The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. (optional)
data_portal = 'data_portal_example' # str | The data portal ID. Defaults to 'ena'. (optional)
dcc_data_only = true # bool | Whether to limit the search to only DCC records. By default, all public data is also included in the search. (optional)
include_metagenomes = true # bool | Whether to include public metagenome data in the search. By default, these are not included. Note that any metagenome data associated with a DCC hub will always be included in a search against that DCC. (optional)
email = 'email_example' # str | Submit search and be notified via email when search result is ready for downloading. Mandatory if fields=all is set. (optional)
saved_search = 'saved_search_example' # str | The id to download the results of a previously submitted search. If this parameter is set, all additional parameters are ignored. (optional)
format = 'format_example' # str | What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. (optional)
download = true # bool | Whether to download the result as a file, rather than read it from the stream. By default, this is false. (optional)

try:
    # Perform a warehouse search with POST
    api_response = api_instance.search_post_using_post(result, query=query, fields=fields, sort_fields=sort_fields, offset=offset, limit=limit, data_portal=data_portal, dcc_data_only=dcc_data_only, include_metagenomes=include_metagenomes, email=email, saved_search=saved_search, format=format, download=download)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->search_post_using_post: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result** | **str**| The result type (data set) to search against. Is mandatory. | 
 **query** | **str**| A set of search conditions joined by logical operators (AND, OR, NOT) and bound by double quotes. If none supplied, the full result set will be returned. | [optional] 
 **fields** | **str**| A list of fields (comma separated) to be returned in the result. If none supplied, the accession and description/title of the main result object will be returned. | [optional] 
 **sort_fields** | **str**| A list of fields (comma separated) in the order of which the results should be sorted. | [optional] 
 **offset** | **int**| How many records to skip from the beginning in the results. Default value is 0. | [optional] 
 **limit** | **int**| The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. | [optional] 
 **data_portal** | **str**| The data portal ID. Defaults to &#39;ena&#39;. | [optional] 
 **dcc_data_only** | **bool**| Whether to limit the search to only DCC records. By default, all public data is also included in the search. | [optional] 
 **include_metagenomes** | **bool**| Whether to include public metagenome data in the search. By default, these are not included. Note that any metagenome data associated with a DCC hub will always be included in a search against that DCC. | [optional] 
 **email** | **str**| Submit search and be notified via email when search result is ready for downloading. Mandatory if fields&#x3D;all is set. | [optional] 
 **saved_search** | **str**| The id to download the results of a previously submitted search. If this parameter is set, all additional parameters are ignored. | [optional] 
 **format** | **str**| What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. | [optional] 
 **download** | **bool**| Whether to download the result as a file, rather than read it from the stream. By default, this is false. | [optional] 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded
 - **Accept**: */*

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_using_get**
> object search_using_get(result, saved_search=saved_search, query=query, fields=fields, sort_fields=sort_fields, offset=offset, limit=limit, data_portal=data_portal, dcc_data_only=dcc_data_only, include_metagenomes=include_metagenomes, format=format, download=download, email=email)

Perform a warehouse search

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.PortalAPIApi(swagger_client.ApiClient(configuration))
result = 'result_example' # str | The result type (data set) to search against. Is mandatory.
saved_search = 'saved_search_example' # str | The id to download the results of a previously submitted search. If this parameter is set, all additional parameters are ignored. (optional)
query = 'query_example' # str | A set of search conditions joined by logical operators (AND, OR, NOT) and bound by double quotes. If none supplied, the full result set will be returned. (optional)
fields = 'fields_example' # str | A list of fields (comma separated) to be returned in the result. If none supplied, the accession and description/title of the main result object will be returned. (optional)
sort_fields = 'sort_fields_example' # str | A list of fields (comma separated) in the order of which the results should be sorted. (optional)
offset = 56 # int | How many records to skip from the beginning in the results. Default value is 0. (optional)
limit = 56 # int | The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. (optional)
data_portal = 'data_portal_example' # str | The data portal ID. Defaults to 'ena'. (optional)
dcc_data_only = true # bool | Whether to limit the search to only DCC records. By default, all public data is also included in the search. (optional)
include_metagenomes = true # bool | Whether to include public metagenome data in the search. By default, these are not included. Note that any metagenome data associated with a DCC hub will always be included in a search against that DCC. (optional)
format = 'format_example' # str | What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. (optional)
download = true # bool | Whether to download the result as a file, rather than read it from the stream. By default, this is false. (optional)
email = 'email_example' # str | Submit search and be notified via email when search result is ready for downloading. Mandatory if fields=all is set. (optional)

try:
    # Perform a warehouse search
    api_response = api_instance.search_using_get(result, saved_search=saved_search, query=query, fields=fields, sort_fields=sort_fields, offset=offset, limit=limit, data_portal=data_portal, dcc_data_only=dcc_data_only, include_metagenomes=include_metagenomes, format=format, download=download, email=email)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PortalAPIApi->search_using_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **result** | **str**| The result type (data set) to search against. Is mandatory. | 
 **saved_search** | **str**| The id to download the results of a previously submitted search. If this parameter is set, all additional parameters are ignored. | [optional] 
 **query** | **str**| A set of search conditions joined by logical operators (AND, OR, NOT) and bound by double quotes. If none supplied, the full result set will be returned. | [optional] 
 **fields** | **str**| A list of fields (comma separated) to be returned in the result. If none supplied, the accession and description/title of the main result object will be returned. | [optional] 
 **sort_fields** | **str**| A list of fields (comma separated) in the order of which the results should be sorted. | [optional] 
 **offset** | **int**| How many records to skip from the beginning in the results. Default value is 0. | [optional] 
 **limit** | **int**| The maximum number of records to retrieve. Default value is 100,000. If the full result set is to be fetched, the limit should be set to 0. | [optional] 
 **data_portal** | **str**| The data portal ID. Defaults to &#39;ena&#39;. | [optional] 
 **dcc_data_only** | **bool**| Whether to limit the search to only DCC records. By default, all public data is also included in the search. | [optional] 
 **include_metagenomes** | **bool**| Whether to include public metagenome data in the search. By default, these are not included. Note that any metagenome data associated with a DCC hub will always be included in a search against that DCC. | [optional] 
 **format** | **str**| What format the results should be returned as: TSV (Tab Separated Values) or JSON. By default, a TSV report is provided. | [optional] 
 **download** | **bool**| Whether to download the result as a file, rather than read it from the stream. By default, this is false. | [optional] 
 **email** | **str**| Submit search and be notified via email when search result is ready for downloading. Mandatory if fields&#x3D;all is set. | [optional] 

### Return type

**object**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: text/plain, application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

