import base64

from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient

class APIClient():

    def __init__(self, connection, configuration):
        # Uncomment when implementing data source API client.
        # auth = configuration.get('auth')

        # headers = dict()
        # headers['X-Auth-Token'] = auth.get('token')
        # self.client = RestApiClient(connection.get('host'),
        #                             connection.get('port'),
        #                             connection.get('cert', None),
        #                             headers,
        #                             cert_verify=connection.get('cert_verify', 'True')
        #                             )

        # Placeholder client to allow dummy transmission calls.
        # Remove when implementing data source API client.

        auth = configuration.get('auth')
        self.orgId = configuration.get('orgId')
        headers = {'Accept': 'application/json'}
        headers['Authorization'] = b"Basic " + base64.b64encode(
            (auth['username'] + ':' + auth['password']).encode('ascii'))
        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port'),
                                    cert_verify=False,
                                    headers = headers,
                                    auth=None
                                    )

        #self.client = "data source API client"

    def ping_data_source(self):
        # Pings the data source
        #return {"code": 200, "success": True}
        return self.client.call_api("/rest/artifacts", 'GET')

    def get_search_results(self, search_id, range_start=None, range_end=None):
        # Return the search results. Results must be in JSON format before being translated into STIX
        return {"code": 200, "data": "Results from search"}

    def delete_search(self, search_id):
        # Optional since this may not be supported by the data source API
        # Delete the search
        return {"code": 200, "success": True}

    def create_search(self, query_expression):
        headers = dict()
        headers['Content-type'] = 'application/json'
        endpoint = "rest/orgs/{orgId}/artifacts/query_paged".format(orgId=self.orgId)
        data = query_expression
        return self.client.call_api(endpoint, 'POST', headers, data=data)

