import logging

import pytest

from integration_tests.constants import HOST, CLIENT_TOKEN
from integration_tests.example_response.aggregation import response_aggregationUnits
from integration_tests.example_response.codes import response_codes
from integration_tests.example_response.issuers import response_issuers
from integration_tests.example_response.orders import response_orders, buffers
from integration_tests.example_response.ping import response_ping
from integration_tests.example_response.report_info import response_report_info
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.api_integration import ApiIntegration
from integration_tests.utils.auth import Auth
from integration_tests.utils.orders import Orders
from integration_tests.utils.report import Report

url_ping = f"{HOST}/api/v2/cml/ping"
url_orders = f"{HOST}/api/v2/cml/orders"
url_report_info = f"{HOST}/api/v2/cml/report/info"
url_codes = f"{HOST}/api/v2/cml/codes"
url_suborder_close = f"{HOST}/api/v2/cml/suborder/close"
url_utilisation = f"{HOST}/api/v2/cml/utilisation"
url_aggregation = f"{HOST}/api/v2/cml/aggregation"
url_issuers = f"{HOST}/api/v2/cml/issuers"


def test_positive_ping():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_ping}")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN}
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


def test_positive_orders():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_orders}")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN}
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


def test_positive_report_info():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_report_info}")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    report_id = Report.get_report_id(jsessionid)
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.get(url_report_info, headers=headers, params={"reportId": report_id})
    mismatch_keys = [key for key in data if key not in response_report_info]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_orders: {key}')

    mismatch_keys1 = [key for key in response_report_info if key not in data]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')
    assert len(mismatch_keys) == 0 and len(mismatch_keys1) == 0
    assert code == 200


def test_negative_report_info_required_reportid():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_report_info}"
                 f" без обязательного параметра запроса reportId")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.get(url_report_info, headers=headers)
    assert code == 400
    assert data['errorCode'] == 400 and data['errorText'] == 'Required String parameter \'reportId\' is not present'


def test_negative_report_info_required_client_token():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_report_info}"
                 f" без токена")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    report_id = Report.get_report_id(jsessionid)
    code, data = api.get(url_report_info, params={"reportId": report_id})
    assert code == 400
    assert data['errorCode'] == 400
    assert data['errorText'] == "Missing request header 'clientToken' for method parameter of type String"
    assert len(data) == 2


def test_positive_get_codes():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_codes}")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
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


def test_negative_get_codes_buffer_not_active():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} при закрытом подзаказе")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "CLOSED")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert code == 400
    assert len(data) == 2
    assert data['errorText'] == 'BufferService.NotActive'


def test_negative_get_codes_required_gtin():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} без обязательного параметра gtin")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    del params_for_get_codes["gtin"]
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Required String parameter \'gtin\' is not present'


def test_negative_get_codes_required_order_id():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} без обязательного параметра orderId")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    del params_for_get_codes["orderId"]
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Required String parameter \'orderId\' is not present'


def test_negative_get_codes_required_quantity():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_codes} без обязательного параметра quantity")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    del params_for_get_codes["quantity"]
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Required int parameter \'quantity\' is not present'


def test_positive_aggregation():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_aggregation} c aggregation_type='AGGREGATION'")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
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
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "UPDATE", quality=["C", "D"])
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
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
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
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
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['sntins'][0]['quality']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'Параметр \'quality\' не может быть пустым'


def test_negative_aggregation_required_unit_serial_number():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса unitSerialNumber")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['unitSerialNumber']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].unitSerialNumber: не может быть пусто'


def test_negative_aggregation_required_aggregation_unit_capacity():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса aggregationUnitCapacity")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregationUnitCapacity']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].aggregationUnitCapacity: должно быть больше или равно 1'


def test_negative_aggregation_required_aggregation_type():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса aggregationType")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregationType']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].aggregationType: должно быть задано'


def test_negative_aggregation_required_aggregated_items_count():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса aggregatedItemsCount")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregatedItemsCount']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    assert data['errorText'] == 'aggregationUnits[0].aggregatedItemsCount: должно быть больше или равно 1'


def test_negative_aggregation_required_code():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c без обязательного параметра запроса code")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['sntins'][0]['code']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    # TODO поправить текст ошибки в коде
    assert data['errorText'] == 'Указаны неверные коды маркировки'


def test_negative_aggregation_required_invalid_quality():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c невалидными параметрами качества")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["Z", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregatedItemsCount']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    str_exists = data['errorText'].find('''"Z": value not one of declared Enum instance names: [A, B, C, D, F]''')
    assert str_exists != -1


def test_negative_aggregation_required_invalid_aggregation_type():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_aggregation} "
                 f"c невалидными параметрами типа аггрегации")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "INVALID_TYPE", quality=["A", "B"])
    del data_aggregation['aggregationUnits'][0]['aggregatedItemsCount']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert len(data) == 2
    assert code == 400
    str_exists = \
        data['errorText'].find('"INVALID_TYPE": value not one of declared Enum instance names: [UPDATE, AGGREGATION]')
    assert str_exists != -1


def test_positive_suborder_close():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_suborder_close}")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    orders = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.post(url=url_suborder_close, headers=headers,
                          params={"orderId": orders['orderId'],
                                  "gtin": orders['gtin']})
    assert code == 200
    assert data['success']
    assert len(data) == 1


def test_negative_suborder_close_buffer_unactive():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_suborder_close} "
                 f"для кодов из закрытого подзаказа")
    logging.info("Незакончен")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    orders = Orders.get_params_for_get_codes(jsessionid, "CLOSED")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.post(url=url_suborder_close, headers=headers,
                          params={"orderId": orders['orderId'],
                                  "gtin": orders['gtin']})
    # TODO дополнить сценарий тем, что этот подзаказ больше недоступен для других операций
    assert code == 200
    assert data['success']
    assert len(data) == 1


def test_negative_suborder_close_required_order_id():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_suborder_close} "
                 f"без обязательного параметра orderId")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    orders = Orders.get_params_for_get_codes(jsessionid, "CLOSED")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.post(url=url_suborder_close, headers=headers,
                          params={"gtin": orders['gtin']})

    assert code == 400
    assert len(data) == 2
    assert data['errorText'] == 'Required String parameter \'orderId\' is not present'


def test_negative_suborder_close_required_gtin():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_suborder_close} "
                 f"без обязательного параметра gtin")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    orders = Orders.get_params_for_get_codes(jsessionid, "CLOSED")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data = api.post(url=url_suborder_close, headers=headers,
                          params={"orderId": orders['orderId']})

    assert code == 400
    assert len(data) == 2
    assert data['errorText'] == 'Required String parameter \'gtin\' is not present'


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


def test_positive_utilisation():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_utilisation}")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_utilisation = ApiIntegration.post_utilisation(data_codes, "VERIFIED")
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_utilisation, headers=headers, json=data_utilisation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert code == 200
    assert data['reportId'] is not None
    assert len(data) == 1


def test_positive_utilisation_any_usage_type():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_utilisation} c usage_type=PRINTED")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_utilisation = ApiIntegration.post_utilisation(data_codes, "PRINTED")
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_utilisation, headers=headers, json=data_utilisation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert code == 200
    assert data['reportId'] is not None
    assert len(data) == 1


def test_negative_utilisation_invalid_usage_type():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_utilisation} c невалидным usage_type")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_utilisation = ApiIntegration.post_utilisation(data_codes, "INVALID")
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_utilisation, headers=headers, json=data_utilisation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert code == 400
    str_include = data['errorText'].find(
        '"INVALID": value not one of declared Enum instance names: [VERIFIED, PRINTED]')
    assert str_include != -1


def test_negative_utilisation_required_oms_id():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_utilisation} без обязательного параметра omsId")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_utilisation = ApiIntegration.post_utilisation(data_codes, "VERIFIED")
    code, data = api.post(url=url_utilisation, headers=headers, json=data_utilisation)
    assert code == 400
    assert data['errorText'] == 'Required String parameter \'omsId\' is not present'


def test_negative_utilisation_required_usage_type():
    logging.info(
        f"Проверка позитивного сценария выполнения запроса {url_utilisation} без обязательного параметра usageType")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_utilisation = ApiIntegration.post_utilisation(data_codes, "PRINTED")
    del data_utilisation['usageType']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_utilisation, headers=headers, json=data_utilisation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert code == 400
    assert data['errorText'] == 'usageType: должно быть задано'


def test_negative_utilisation_required_sntins():
    logging.info(
        f"Проверка позитивного сценария выполнения запроса {url_utilisation} без обязательного параметра sntins")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, "ACTIVE")
    headers = {"clientToken": CLIENT_TOKEN}
    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_utilisation = ApiIntegration.post_utilisation(data_codes, "PRINTED")
    del data_utilisation['sntins']
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_utilisation, headers=headers, json=data_utilisation,
                          params={"omsId": orders[1]['result'][0]['omsId']})
    assert code == 400
    assert data['errorText'] == 'sntins: размер должен быть между 1 и 30000'
