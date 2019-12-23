import logging

from integration_tests.constants import CLIENT_TOKEN_KD, STAND_KD
from integration_tests.example_response.orders import response_orders, buffers
from integration_tests.utils.api_helpers import ClientApi


url_orders = f"{STAND_KD}/api/v2/cml/orders"
url_codes = f"{STAND_KD}/api/v2/cml/codes"


def test_positive_orders():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_orders}")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url_orders, headers=headers)
    assert code == 200
    mismatch_keys = [key for key in data['orderInfos'][0] if key not in response_orders]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_orders: {key}')

    mismatch_keys1 = [key for key in response_orders if key not in data['orderInfos'][0]]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')

    assert set(data['orderInfos'][0].keys()) == set(response_orders.keys())
    buffers_key = [key for key in buffers if key not in data['orderInfos'][0]['buffers'][0]]
    buffers_key_1 = [key for key in data['orderInfos'][0]['buffers'][0] if key not in buffers]
    assert len(buffers_key) == 0 and len(buffers_key_1) == 0


def test_negative_orders():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_orders} без токена")
    api = ClientApi()
    code, data = api.get(url_orders)
    assert code == 400
    assert data['errorCode'] == 400
    assert data['errorText'] == "Missing request header 'clientToken' for method parameter of type String"