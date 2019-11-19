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
        return code, data

    @staticmethod
    def get_params_for_get_codes(jsessionid, bufferStatus):
        code, data = Orders.get_orders(jsessionid)
        params_for_get_codes = None
        for result in data['result']:
            for buffers in result['buffers']:
                if buffers['bufferStatus'] == bufferStatus:
                    params_for_get_codes = {
                        "gtin": buffers['gtin'],
                        "lastBlockId": "0",
                        "orderId": result['orderId'],
                        "quantity": 2}
                    break
        if params_for_get_codes is not None:
            return params_for_get_codes
        else:
            logging.info(f"Нет кодов со статусом:{bufferStatus}")
            assert False


