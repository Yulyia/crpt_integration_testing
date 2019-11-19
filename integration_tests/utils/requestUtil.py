import logging
import requests


class RequestUtil:
    @staticmethod
    def request(method, url, **kwargs):
        try:
            logging.debug(f'method: {method} url: {url}')
            logging.debug(kwargs)

            resp = requests.request(method, url, **kwargs)

            if resp.status_code < 400:
                logging.debug(f"resp.status_code: {resp.status_code} resp.json {resp.json()}")
            elif resp.status_code > 499:
                logging.error(f"resp.status_code: {resp.status_code} resp.json {resp.json()}")
            else:
                logging.warning(f"resp.status_code: {resp.status_code} resp.json {resp.json()}")

            return resp

        except Exception as e:
            logging.error(e)

        return resp