import logging

from integration_tests.constants import HOST, CLIENT_TOKEN
from integration_tests.example_response.issuers import response_issuers
from integration_tests.utils.api_helpers import ClientApi

url_issuers = f"{HOST}/api/v2/cml/issuers"


def test_positive_issuers():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_issuers} (получение эмитентов)")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.get(url_issuers, headers=headers)
    assert code == 200
    mismatch_keys = [key for key in data[0] if key not in response_issuers]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_ping: {key}')

    mismatch_keys1 = [key for key in response_issuers if key not in data[0]]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')
    assert len(mismatch_keys) == 0 and len(mismatch_keys1) == 0


def test_negative_issuers():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_issuers} (получение эмитентов) без токена")
    api = ClientApi()
    code, data = api.get(url_issuers)
    assert code == 400
    assert data['errorText'] == 'Missing request header \'clientToken\' for method parameter of type String'
