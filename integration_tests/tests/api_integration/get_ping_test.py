import logging
from integration_tests.constants import CLIENT_TOKEN_INCORRECT, CLIENT_TOKEN_KD, STAND_KD
from integration_tests.example_response.ping import response_ping
from integration_tests.utils.api_helpers import ClientApi

url_ping = f"{STAND_KD}/api/v2/cml/ping"


def test_positive_ping():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_ping}")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url_ping, headers=headers)
    assert code == 200
    mismatch_keys = [key for key in data if key not in response_ping]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_ping: {key}')

    mismatch_keys1 = [key for key in response_ping if key not in data]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')

    assert set(data.keys()) == set(response_ping.keys())


def test_negative_ping():
    logging.info(f"Проверка негативного выполнения запроса {url_ping} без токена")
    api = ClientApi()
    code, data = api.get(url_ping)
    assert code == 400
    assert data['errorCode'] == 400
    assert data['errorText'] == "Missing request header 'clientToken' for method parameter of type String"


def test_negative_ping_incorrect_token():
    logging.info(f"Проверка негативного выполнения запроса {url_ping} без токена")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN_INCORRECT}
    code, data = api.get(url_ping, headers=headers)
    assert code == 400
    assert data['errorCode'] == 400
    assert data['errorText'] == 'Указан неверный client token'