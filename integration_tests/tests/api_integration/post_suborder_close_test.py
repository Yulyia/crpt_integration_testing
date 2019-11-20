import logging


from integration_tests.constants import HOST, CLIENT_TOKEN
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.auth import Auth
from integration_tests.utils.orders import Orders

url_codes = f"{HOST}/api/v2/cml/codes"
url_suborder_close = f"{HOST}/api/v2/cml/suborder/close"


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




