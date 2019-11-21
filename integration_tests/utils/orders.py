import logging

from integration_tests.utils.api_helpers import ClientApi
from integration_tests.constants import HOST

orders_url_in_kd = f"{HOST}/webapi/v1/orders"
params = {"limit": 10, "skip": 0, "total": 0, "sort": ""}


class Orders:
    @staticmethod
    def get_orders(jsessionid):
        api = ClientApi()
        code, data = api.get(url=orders_url_in_kd, params=params, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        # if data['totalCount'] > 10:
        #     params1 = {"limit": 10, "skip": 10, "total": 0, "sort": ""}
        #     code, data = api.get(url=orders_url_in_kd, params=params1, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data

    @staticmethod
    def get_params_for_get_codes(jsessionid, bufferStatus, quantity=2, leftInBuffer=None):
        code, data = Orders.get_orders(jsessionid)
        params_for_get_codes = None
        for result in data['result']:
            if params_for_get_codes is not None:
                break
            for buffers in result['buffers']:
                if leftInBuffer is not None:
                    if buffers['bufferStatus'] == bufferStatus and buffers['leftInBuffer'] == leftInBuffer:
                        params_for_get_codes = {
                            "gtin": buffers['gtin'],
                            "lastBlockId": "0",
                            "orderId": result['orderId'],
                            "quantity": quantity}
                        break
                if buffers['bufferStatus'] == bufferStatus == 'ACTIVE' and buffers['leftInBuffer'] >= quantity:
                    params_for_get_codes = {
                        "gtin": buffers['gtin'],
                        "lastBlockId": "0",
                        "orderId": result['orderId'],
                        "quantity": quantity}
                    break
                if buffers['bufferStatus'] == bufferStatus == 'CLOSED':
                    params_for_get_codes = {
                        "gtin": buffers['gtin'],
                        "lastBlockId": "0",
                        "orderId": result['orderId'],
                        "quantity": quantity}
                    break
        if params_for_get_codes is not None:
            logging.info(f"Параметры заказа для получения КМ: orderId - [{params_for_get_codes['orderId']}] "
                         f"gtin - [{params_for_get_codes['gtin']}] "
                         f"quantity - [{params_for_get_codes['quantity']}]")
            return params_for_get_codes
        else:
            logging.info(f"Нет кодов со статусом:{bufferStatus} и нужным кол-м КМ в буфере")
            assert False
