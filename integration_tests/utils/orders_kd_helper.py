import logging

from integration_tests.types.bufferstatus import BufferStatus
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.constants import STAND_KD

orders_url_in_kd = f"{STAND_KD}/webapi/v1/orders"
order_info_url = f"{STAND_KD}/webapi/v1/orders/[id_orders]"
order_info_buffer_url = f"{STAND_KD}/webapi/v1/orders/buffer/[id_orders]"
order_close_url = f"{STAND_KD}/webapi/v1/orders/close"


params = {"limit": 50, "skip": 0, "total": 0, "sort": ""}


def get_filters(quantity: int = 0):
    return (
        (BufferStatus.ACTIVE_STATUS.value, lambda i: i['leftInBuffer'] >= quantity),
        (BufferStatus.CLOSED_STATUS.value, lambda i: True),
        (BufferStatus.ACTIVE_STATUS_EMPTY.value, lambda i: i['leftInBuffer'] == 0)
    )


def get_filters_for_one_buffer(status, quantity: int = 0):
    if status == BufferStatus.ACTIVE_STATUS and quantity == 0:
        return BufferStatus.ACTIVE_STATUS.value, lambda i: i['leftInBuffer'] == 0
    if status == BufferStatus.ACTIVE_STATUS:
        return BufferStatus.ACTIVE_STATUS.value, lambda i: i['leftInBuffer'] >= quantity
    if status == BufferStatus.CLOSED_STATUS:
        return BufferStatus.CLOSED_STATUS.value, lambda i: True


def filter_buffers(order, status, check):
    return len(list(filter(
        lambda buffer: (
            buffer['bufferStatus'] == status and check(buffer)),
        order.get('buffers', [])
    ))) > 0


class Orders:
    @staticmethod
    def get_orders(jsessionid):
        api = ClientApi()
        code, data = api.get(url=orders_url_in_kd, params=params, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data

    @staticmethod
    def get_order_by_id(jsessionid, id_order):
        api = ClientApi()
        code, data = api.get(url=orders_url_in_kd, params=params, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        for order in data['result']:
            if order['orderId'] == id_order:
                return order

    @staticmethod
    def get_orders_all_check(jsessionid, quantity=2):
        code, data = Orders.get_orders(jsessionid)
        filters = get_filters(quantity)
        active_buffers, closed_buffers, active_empty_buffers = [
            list(filter(
                lambda order: filter_buffers(order, status, check),
                data['result']
            ))
            for status, check in filters
        ]
        return active_buffers, closed_buffers, active_empty_buffers

    @staticmethod
    def get_params_for_get_codes(jsessionid, buffer_status, quantity=2):
        code, data = Orders.get_orders(jsessionid)
        filter_1 = get_filters_for_one_buffer(buffer_status, quantity)
        order_check = list(filter(lambda order: filter_buffers(order, filter_1[0], filter_1[1]), data['result']))
        gtin = []
        if len(order_check) > 0:
            for buffer in order_check[0]['buffers']:
                if buffer['bufferStatus'] == buffer_status.value and buffer['leftInBuffer'] >= quantity:
                    gtin.append(buffer['gtin'])
            params_for_get_codes = {
                "gtin": gtin[0],
                "lastBlockId": "0",
                "orderId": order_check[0]['orderId'],
                "quantity": quantity}
            logging.info(f"Параметры заказа для получения КМ: orderId - [{params_for_get_codes['orderId']}] "
                         f"gtin - [{params_for_get_codes['gtin']}] "
                             f"quantity - [{params_for_get_codes['quantity']}]")
            return params_for_get_codes
        else:
            logging.info(f"Нет кодов со статусом:{buffer_status} и нужным кол-м КМ в буфере: {quantity}")
            assert False

    @staticmethod
    def get_order_info(product_group, jsessionid):
        api = ClientApi()
        code, data = Orders.get_orders(jsessionid)
        for order in data['result']:
            if order['productGroupType'] == product_group:
                order_id = order['orderId']
                break
        if order_id is None:
            logging.info(f"Нет подходящего заказа с товарной группой {product_group}")
            assert False
        url = order_info_url.replace('[id_orders]', order_id)
        code, data = api.get(url, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data

    @staticmethod
    def get_order_buffer_info(jsessionid):
        api = ClientApi()
        code, data = Orders.get_orders(jsessionid)
        url = order_info_buffer_url.replace('[id_orders]', data['result'][0]['orderId'])
        code, data = api.get(url, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data

    @staticmethod
    def close_order(jsessionid):
        api = ClientApi()
        code, data = Orders.get_orders(jsessionid)
        data = {'orderId': data['result'][0]['orderId']}
        code, data = api.post(order_close_url, json=data, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data









