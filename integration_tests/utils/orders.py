import logging

from integration_tests.utils.api_helpers import ClientApi
from integration_tests.constants import HOST

orders_url_in_kd = f"{HOST}/webapi/v1/orders"
params = {"limit": 10, "skip": 0, "total": 0, "sort": ""}


ACTIVE_STATUS = 'ACTIVE'
ACTIVE_STATUS_EMPTY = 'ACTIVE'
CLOSED_STATUS = 'CLOSED'


def get_filters(quantity: int = 0):
    return (
        (ACTIVE_STATUS, lambda i: i['leftInBuffer'] >= quantity),
        (CLOSED_STATUS, lambda i: True),
        (ACTIVE_STATUS_EMPTY, lambda i: i['leftInBuffer'] == 0)
    )


def filter_buffers(order, status, check):
    return len(list(filter(
        lambda buffer: (
            buffer['bufferStatus'] == status and check(buffer)),
        order.get('buffers', [])
    ))) > 0


class Orders:
    @staticmethod
    def get_all_orders(jsessionid):
        api = ClientApi()
        code, data = api.get(url=orders_url_in_kd, params=params, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data

    @staticmethod
    def get_orders_check(jsessionid, quantity=2):
        code, data = Orders.get_all_orders(jsessionid)
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
    def get_params():
        pass
        # params_for_get_codes = {
        #     "gtin": buffers['gtin'],
        #     "lastBlockId": "0",
        #     "orderId": result['orderId'],
        #     "quantity": quantity}
        # if params_for_get_codes is not None:
        #     logging.info(f"Параметры заказа для получения КМ: orderId - [{params_for_get_codes['orderId']}] "
        #                  f"gtin - [{params_for_get_codes['gtin']}] "
        #                  f"quantity - [{params_for_get_codes['quantity']}]")
        #     return params_for_get_codes
        # else:
        #     logging.info(f"Нет кодов со статусом:{bufferStatus} и нужным кол-м КМ в буфере")
        #     assert False
