import logging

from integration_tests.constants import CLIENT_TOKEN_KD, STAND_KD
from integration_tests.example_response.codes import response_codes
from integration_tests.types.bufferstatus import BufferStatus
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.auth import Auth
from integration_tests.utils.orders import Orders

url_codes = f"{STAND_KD}/api/v2/cml/codes"


def test_positive_get_codes():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_codes}")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    mismatch_keys = [key for key in data if key not in response_codes]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_orders: {key}')

    mismatch_keys1 = [key for key in response_codes if key not in data]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')
    assert len(mismatch_keys) == 0 and len(mismatch_keys1) == 0
    assert len(data['codes']) == 2
    assert code == 200


def test_positive_get_codes_not_repeat_codes():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_codes}")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS, quantity=1)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data1 = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    code, data2 = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert code == 200
    assert data1['codes'][0] != data2['codes'][0]
    assert data1['blockId'] != data2['blockId']


def test_negative_get_codes_buffer_not_active():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} при закрытом подзаказе")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.CLOSED_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert code == 400
    assert len(data) == 2
    assert data['errorText'] == 'BufferService.NotActive' or "Буфер не активен"


def test_negative_get_codes_required_gtin():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} без обязательного параметра gtin")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    del params_for_get_codes["gtin"]
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Required String parameter \'gtin\' is not present'


def test_negative_get_codes_required_order_id():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} без обязательного параметра orderId")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    del params_for_get_codes["orderId"]
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Required String parameter \'orderId\' is not present'


def test_negative_get_codes_required_quantity():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} без обязательного параметра quantity")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    del params_for_get_codes["quantity"]
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Required int parameter \'quantity\' is not present'












