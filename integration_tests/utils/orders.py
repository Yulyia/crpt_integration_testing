import logging

from integration_tests.types.bufferstatus import BufferStatus
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.constants import HOST

orders_url_in_kd = f"{HOST}/webapi/v1/orders"
params = {"limit": 10, "skip": 0, "total": 0, "sort": ""}


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
        for buffer in order_check[0]['buffers']:
            if buffer['bufferStatus'] == buffer_status.value and buffer['leftInBuffer'] >= quantity:
                gtin.append(buffer['gtin'])
        if len(order_check) > 0:
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
            logging.info(f"Нет кодов со статусом:{buffer_status} и нужным кол-м КМ в буфере")
            assert False



