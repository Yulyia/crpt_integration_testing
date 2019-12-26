import time

from integration_tests.constants import CLIENT_TOKEN_SUZ, STAND, CLIENT_TOKEN_KD
from integration_tests.tests.api_integration.get_codes_test import url_codes
from integration_tests.tests.api_integration.post_aggregation_test import url_aggregation
from integration_tests.tests.api_integration.post_suborder_close_test import url_suborder_close
from integration_tests.tests.api_integration.post_utilisation_test import url_utilisation
from integration_tests.tests.orders.get_orders_SUZ import GTIN_TOBACCO, GTIN_PHARMA, URL_GET_ORDERS_TOBACCO, \
    URL_GET_ORDERS_PHARMA
from integration_tests.types.bufferstatus import BufferStatus
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.api_integration import ApiIntegration
from integration_tests.utils.auth import Auth
from integration_tests.utils.orders_suz_helper import OrderProductTobacco, OrderProductPharma
from integration_tests.utils.fixtures import *
from integration_tests.utils.orders_kd_helper import Orders


def test_stand_activate(contractor_id):
    quantity = 50
    api = ClientApi()
    if STAND == "dev":
        GTIN_TOBACCO = ["12345678901234", "98765432104321", "11111111111111"]

    '''Получение заказа табака'''

    request = OrderProductTobacco.get_order_for_tobacco_request(GTIN_TOBACCO, quantity)
    param = {'omsId': contractor_id}
    headers = {'clientToken': CLIENT_TOKEN_SUZ}
    code, data = api.post(url=URL_GET_ORDERS_TOBACCO, headers=headers, params=param,
                          json=request, verify=False)
    assert code == 200

    '''Получение заказа фармы'''

    request = OrderProductPharma.get_order_for_pharma_request(GTIN_PHARMA, quantity)
    code, data = api.post(url=URL_GET_ORDERS_PHARMA, headers=headers, params=param,
                          json=request, verify=False)
    assert code == 200
    jsessionid = Auth.get_jssesion_id()
    code, data = Orders.get_orders(jsessionid)

    ''' Ожидание, пока заказа появятся в КД'''

    while data['totalCount'] == 0:
        time.sleep(5)
        code, data = Orders.get_orders(jsessionid)
    params_for_get_codes = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS, quantity=quantity)
    headers = {"clientToken": CLIENT_TOKEN_KD}

    ''' Получение отчёта об аггрегации'''

    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_aggregation = ApiIntegration.post_aggregation(data_codes, "AGGREGATION", quality=["A", "B"])
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_aggregation, headers=headers, json=data_aggregation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert code == 200

    ''' Получение отчёта об утилизации'''

    code, data_codes = api.get(url=url_codes, params=params_for_get_codes, headers=headers)
    data_utilisation = ApiIntegration.post_utilisation(data_codes, "VERIFIED")
    orders = Orders.get_orders(jsessionid)
    code, data = api.post(url=url_utilisation, headers=headers, json=data_utilisation,
                          params={"omsId": orders[1]['result'][0]['issuerId']})
    assert code == 200

    ''' Закрытие одного подзаказа '''

    orders = Orders.get_params_for_get_codes(jsessionid, BufferStatus.ACTIVE_STATUS)
    code, data = api.post(url=url_suborder_close, headers=headers,
                          params={"orderId": orders['orderId'],
                                  "gtin": orders['gtin']})
    assert code == 200


