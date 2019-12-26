import logging

from integration_tests.utils.auth import Auth
from integration_tests.utils.orders_kd_helper import Orders


def test_positive_ger_orders():
    logging.info(f"Проверка позитивного сценария получения данных всех заказов")
    jsessionid = Auth.get_jssesion_id()
    code, data = Orders.get_orders(jsessionid)
    assert code == 200
    assert data['result'][0]['issuerName'] is not None
    assert data['result'][0]['issuerInn'] is not None
    assert data['result'][0]['orderStatus'] == 'READY'


def test_positive_get_order_info_tobacco():
    logging.info(f"Проверка позитивного сценария получения расширенных данных заказа")
    jsessionid = Auth.get_jssesion_id()
    code, data = Orders.get_order_info(product_group="TOBACCO", jsessionid=jsessionid)
    assert code == 200
    assert data['orderInfo']['factoryId'] is not None
    assert data['orderInfo']['factoryName'] is not None
    assert data['orderInfo']['factoryAddress'] is not None
    assert data['orderInfo']['factoryCountry'] is not None
    assert data['orderInfo']['productionLineId'] is not None
    assert data['orderInfo']['productCode'] is not None
    assert data['orderInfo']['productDescription'] is not None
    assert data['orderInfo']['poNumber'] is not None


def test_positive_get_order_info_buffer():
    logging.info(f"Проверка позитивного сценария получения расширенных данных буфера заказа")
    jsessionid = Auth.get_jssesion_id()
    code, data = Orders.get_order_buffer_info(jsessionid=jsessionid)
    assert code == 200
    assert data[0]['status'] is not None


def test_positive_close_order():
    logging.info(f"Проверка позитивного сценария закрытия заказа")
    jsessionid = Auth.get_jssesion_id()
    code, data = Orders.close_order(jsessionid=jsessionid)
    assert code == 200
    order = Orders.get_order_by_id(jsessionid, id_order=data['id'])
    assert order['orderStatus'] == "CLOSED"







