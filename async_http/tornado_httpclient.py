import traceback
from urllib.parse import urljoin

import aiohttp
import async_timeout
from tornado.escape import json_decode, json_encode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.httputil import url_concat

GET = 'GET'
POST = 'POST'
TIMEOUT = 180


class HttpCalls:

    def __init__(self, base_url: str, port=None):
        self.base_url = base_url
        if port is not None:
            self.port = str(port)

    async def post(self, route, data, query=dict()):

        if "http" not in route:
            url = urljoin(self.base_url, route)
        else:
            url = route
        return await self.request(POST, url, data=data, params=query)

    async def get(self, route: str, query=dict()) -> object:

        if "http" not in route:
            url = urljoin(self.base_url, route)
        else:
            url = route
        return await self.request(GET, url, params=query)

    def download(self, route):
        return aiohttp.ClientSession().get(urljoin(self.base_url, route))

    async def request(self, method, url, data=None, params=dict()) -> object:
        client = AsyncHTTPClient()
        if data is not None:
            data = json_encode(data)
        try:
            def handle_response(response):
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

                headers = {'Content-Type': 'application/json'}

                url = url_concat(url, params)

                resp = await client.fetch(
                    HTTPRequest(
                        url=url,
                        headers=headers,
                        method=method,
                        body=data
                    )
                )

                if resp.headers['Content-Type'] == 'application/json':
                    body = json_decode(resp.body)
                else:
                    body = resp.body

                return handle_response(body)

        except HTTPError as ex:
            traceback.print_exc()
            pass
        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            client.close()


class APIException(Exception):
    pass
