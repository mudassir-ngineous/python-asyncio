import asyncio
import traceback
from urllib.parse import urljoin

import aiohttp
import async_timeout
from tornado.escape import json_decode, json_encode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPError
from tornado.httputil import url_concat

GET = 'GET'
POST = 'POST'
TIMEOUT = 120000

MAX_RETRY = 3

class HttpCalls:

    def __init__(self, base_url: str, port=None):
        self.base_url = base_url
        if port is not None:
            self.port = str(port)

    async def post(self, route, data, query=dict()):

        url = None
        if "http" not in route:
            url = urljoin(self.base_url, route)
        else:
            url = route
        return await self.request(POST, url, data=data, params=query)

    async def get(self, route: str, query=dict()) -> object:

        url = None
        if "http" not in route:
            url = urljoin(self.base_url, route)
        else:
            url = route
        return await self.request(GET, url, params=query)

    def download(self, route):
        return aiohttp.ClientSession().get(urljoin(self.base_url, route))

    async def request(self, method, url, data=None, params=dict()) -> object:
        client = AsyncHTTPClient()
        done = False
        retries = 0
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


            url = url_concat(url, params)
            headers = {'Content-Type': 'application/json'}
            req = HTTPRequest(
                url=url,
                headers=headers,
                method=method,
                body=data
            )

            async def fetch():
                nonlocal retries, req, done
                retries += 1
                with async_timeout.timeout(120):

                    resp = await client.fetch(req)

                    if resp.headers['Content-Type'] == 'application/json':
                        body = json_decode(resp.body)
                    else:
                        body = resp.body

                    done = True
                    return handle_response(body)

            return await fetch()

        except asyncio.TimeoutError as ex:
            if retries <= MAX_RETRY:
                return await fetch()
            else:
                traceback.print_exc()
                raise ex
        except HTTPError as ex:
            if retries <= 3:
                return await fetch()
            else:
                traceback.print_exc()
                raise ex

        except Exception as ex:
            traceback.print_exc()
            raise ex
        finally:
            if done:
                client.close()


class APIException(Exception):
    pass
