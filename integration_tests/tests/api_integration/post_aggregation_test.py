import logging

from integration_tests.constants import CLIENT_TOKEN_KD, STAND_KD
from integration_tests.example_response.aggregation import response_aggregationUnits
from integration_tests.types.bufferstatus import BufferStatus
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.api_integration import ApiIntegration
from integration_tests.utils.auth import Auth
from integration_tests.utils.orders_kd_helper import Orders


url_aggregation = f"{STAND_KD}/api/v2/cml/aggregation"
url_codes = f"{STAND_KD}/api/v2/cml/codes"


def test_positive_aggregation():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_aggregation} c aggregation_type='AGGREGATION'")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert code == 200
    mismatch_keys = [key for key in data if key not in response_aggregationUnits]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_orders: {key}')
    mismatch_keys1 = [key for key in response_aggregationUnits if key not in data]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')
    assert len(mismatch_keys) == 0 and len(mismatch_keys1) == 0


def test_positive_aggregation_any_params():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_aggregation} c aggregation_type='UPDATE'")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "UPDATE", quality=["C", "D"])
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert code == 200
    mismatch_keys = [key for key in data if key not in response_aggregationUnits]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_orders: {key}')
    mismatch_keys1 = [key for key in response_aggregationUnits if key not in data]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')
    assert len(mismatch_keys) == 0 and len(mismatch_keys1) == 0


def test_negative_aggregation_required_oms_id():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса omsId")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation)
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Required String parameter \'omsId\' is not present'


def test_negative_aggregation_required_quality():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса quality")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['sntins'][0]['quality']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Параметр \'quality\' не может быть пустым'


def test_negative_aggregation_required_unit_serial_number():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса unitSerialNumber")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['unitSerialNumber']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].unitSerialNumber: не может быть пусто'


def test_negative_aggregation_required_aggregation_unit_capacity():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса aggregationUnitCapacity")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregationUnitCapacity']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].aggregationUnitCapacity: должно быть больше или равно 1'


def test_negative_aggregation_required_aggregation_type():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса aggregationType")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregationType']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].aggregationType: должно быть задано'


def test_negative_aggregation_required_aggregated_items_count():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса aggregatedItemsCount")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregatedItemsCount']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].aggregatedItemsCount: должно быть больше или равно 1'


def test_negative_aggregation_required_code():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса code")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['sntins'][0]['code']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    # TODO поправить текст ошибки в коде
    assert data['errorText'] == 'Указаны неверные коды маркировки'


def test_negative_aggregation_invalid_quality():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c невалидными параметрами качества")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["Z", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregatedItemsCount']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    str_exists = data['errorText'].find('''"Z": not one of the values accepted for Enum class: [A, B, C, D, F]''')
    assert str_exists != -1


def test_negative_aggregation_required_invalid_aggregation_type():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c невалидными параметрами типа аггрегации")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "INVALID_TYPE", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregatedItemsCount']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert len(data) == 2
    assert code == 400
    str_exists = \
        data['errorText'].find('"INVALID_TYPE": not one of the values accepted for Enum class: [UPDATE, AGGREGATION]')
    assert str_exists != -1