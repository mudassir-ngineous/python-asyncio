import json
from urllib.parse import urljoin

import aiohttp
import async_timeout
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

requests.adapters.DEFAULT_RETRIES = 3
GET = 0
POST = 1
TIMEOUT = 120
RETRIES = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[500, 502, 503, 504, 400, 404])


class HttpCalls:

    def __init__(self, base_url: str, port=None):
        self.base_url = base_url
        if port is not None:
            self.port = str(port)

    def post(self, route, data, query=dict()):

        url = None
        if "http" not in route:
            url = urljoin(self.base_url, route)
        else:
            url = route
        return self.request(POST, url, data=data, params=query)

    def get(self, route: str, query=dict()) -> object:

        url = None
        if "http" not in route:
            url = urljoin(self.base_url, route)
        else:
            url = route
        return self.request(GET, url, params=query)

    def download(self, route):
        return aiohttp.ClientSession().get(urljoin(self.base_url, route))

    async def request(self, method, url, data=None, params=dict()) -> object:
        try:
            def handleResponse(response):
                if 'status' in response and \
                        'code' in response['status'] and \
                        200 <= int(response['status']['code']) <= 299:

                    return response

                else:
                    error = response['status'].get('err', {}) or \
                            response['status'].get('error', {}) or \
                            response['status'].get('message', {}) or \
                            url + " request failed with " + response['status'].get('code', 400) + " response"

                    raise APIException(error)

            with async_timeout.timeout(TIMEOUT):
                async with aiohttp.ClientSession(json_serialize=json.dumps) as s:
                    headers = {'Content-Type': 'application/json'}

                    if method == GET:
                        async with s.get(url, headers=headers, params=params) as resp:
                            if resp.headers['Content-Type'] == 'application/json':
                                r = await resp.json()
                            else:
                                r = await resp.text()

                            assert resp.status == 200, dict(url=url, params=params,
                                                            message="Assertion \'resp.status == 200\' Failed", resp=r)
                            return handleResponse(r)
                    elif method == POST:
                        async with s.post(url, json=data, params=params, headers=headers) as resp:
                            if resp.headers['Content-Type'] == 'application/json':
                                r = await resp.json()
                            else:
                                r = await resp.text()

                            assert resp.status == 200, dict(url=url, data=data, params=params, resp=r,
                                                            message="Assertion \'resp.status == 200\' Failed")
                            return handleResponse(r)

        except Exception as ex:
            raise ex


class APIException(Exception):
    pass