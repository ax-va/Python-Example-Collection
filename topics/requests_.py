"""
This example is based on:
- "Data Visualization with Python and JavaScript: Scrape, Clean, Explore, and Transform Your Data", Kyran Dale, O'Reilly, 2023;
- https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
- https://requests.readthedocs.io/en/latest/user/quickstart/

Upgrade certifi:
pip install --upgrade certifi

Run IPython with the customer OpenSSL configuration to avoid
the "unsafe legacy renegotiation disabled" error for "stats.oecd.org":
OPENSSL_CONF=./openssl/unsafe_legacy_renegotiation.cnf ipython
That error is caused by:
the server doesn't support "secure renegotiation"
and the client is using OpenSSL 3.
For a cleaner solution, use requests.Session():
https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled
https://requests.readthedocs.io/en/latest/user/advanced/#transport-adapters
"""
import json
import requests

print(requests.__version__)
# 2.31.0

response = requests.get("https://en.wikipedia.org/wiki/Nobel_Prize")
response.status_code
# 200

# 401 (Unauthorized)            attempting unauthorized access
# 400 (Bad Request)             trying to access the web server incorrectly
# 403 (Forbidden)               similar to 401 but no login opportunity was available
# 404 (Not Found)               trying to access a web page that doesn't exist
# 500 (Internal Server Error)   a general-purpose, catchall error

response.headers
# {
#   'date': 'Sat, 14 Oct 2023 15:32:23 GMT',
#   'vary': 'Accept-Encoding,Cookie',
#   'server': 'ATS/9.1.4',
#   'x-content-type-options': 'nosniff',
#   'content-language': 'en',
#   'accept-ch': '',
#   'last-modified': 'Fri, 13 Oct 2023 15:22:29 GMT',
#   'content-type': 'text/html; charset=UTF-8',
#   'content-encoding': 'gzip',
#   'age': '66002',
#   'x-cache': 'cp3068 miss, cp3068 hit/26',
#   'x-cache-status': 'hit-front',
#   'server-timing': 'cache;desc="hit-front", host;desc="cp3068"',
# ...

response.text
# '<!DOCTYPE html>\n<html class="client-nojs ...

# There is the three main types of APIs:
# - REST: REpresentational State Transfer = combination of HTTP verbs (GET, POST, etc.) and Uniform Resource Identifiers (URIs; e.g., /user/new);
# - XML-RPC: remote procedure call (RPC) protocol + XML encoding + HTTP transport;
# - SOAP: Simple Object Access Protocol + XML + HTTP.

# RESTful APIs: CRUD (create, retrieve, update, delete) with the POST, GET, PUT, and DELETE verbs

# See API documentation: https://data.oecd.org/api/sdmx-json-documentation/
# Call https://stats.oecd.org/sdmx-json/data/QNA/AUS+AUT.GDP+B1_GE.CUR+VOBARSA.Q/all?startTime=2009-Q1&endTime=2011-Q4
OECD_BASE_URL = 'http://stats.oecd.org/sdmx-json/data'
url = OECD_BASE_URL + '/QNA/AUS+AUT.GDP+B1_GE.CUR+VOBARSA.Q/all?'
response = requests.get(url=url, params={'startTime': '2009-Q1', 'endTime': '2011-Q4'})
# <Response [200]>

if response.status_code == 200:
    response_dict = response.json()
    response_dict.keys()
    # dict_keys(['header', 'dataSets', 'structure'])
    # Data in the SDMX format: https://en.wikipedia.org/wiki/SDMX
    # See also https://pypi.org/project/pandaSDMX/

RESTCOUNTRIES_BASE_URL = "https://restcountries.com/v3.1"
# Some sites will the request without user agent
headers={'User-Agent': 'Mozilla/5.0'}
url = RESTCOUNTRIES_BASE_URL + "/currency" + "/usd"
response = requests.get(url=url, headers=headers)
#  <Response [200]>

url = RESTCOUNTRIES_BASE_URL + "/all"
response = requests.get(url=url, headers=headers)
# <Response [200]>

# Save data in JSON
with open('json-files/world-country-data.json', 'w') as json_file:
    json.dump(response.json(), json_file)
