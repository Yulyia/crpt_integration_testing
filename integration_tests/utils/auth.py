import logging

from integration_tests.utils.requestUtil import RequestUtil
from integration_tests.constants import HOST


URL_AUTH = f"{HOST}/webapi/v1/auth"
LOGIN = "admin"
PASSWORD = "admin"


class Auth:
    @staticmethod
    def get_jssesion_id():
        resp = RequestUtil.request("POST", URL_AUTH, json={"id": LOGIN, "password": PASSWORD})
        logging.info(f"Авторизация на портале с логином {LOGIN} и паролем {PASSWORD}")
        jsessionid = resp.cookies.get('JSESSIONID')
        return jsessionid
