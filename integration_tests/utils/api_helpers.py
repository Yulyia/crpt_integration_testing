from integration_tests.utils.requestUtil import RequestUtil
from json import JSONDecodeError


class ClientApi:
    def __init__(self, client=None):
        if client is not None:
            self.token = client.token

    def get(self, url="", data=None, headers=None, **kwargs):
        return self.call(method="GET", url=url, data=data, headers=headers, **kwargs)

    def post(self, url="", json=None, data=None,  headers=None,**kwargs):
        return self.call(method="POST", url=url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url="", json=None, data=None, headers=None,**kwargs):
        return self.call(method="DELETE", url=url, data=data, json=json, headers=headers, **kwargs)

    def patch(self, url="", json=None, data=None, headers=None, **kwargs):
        return self.call(method="PATCH", url=url, data=data, json=json, headers=headers, **kwargs)

    def call(self, method="GET", url="", data=None, headers=None, **kwargs):

        if headers is not None:
            headers = headers
        else:
            headers = dict()

        resp = RequestUtil.request(
            method, url, data=data, headers=headers, **kwargs)

        try:
            return resp.status_code, resp.json()
        except JSONDecodeError:
            return resp.status_code, resp.content.decode()
        except:
            return resp.status_code, None
