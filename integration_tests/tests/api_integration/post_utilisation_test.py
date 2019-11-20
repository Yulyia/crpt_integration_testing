import logging

import pytest

from integration_tests.constants import HOST, CLIENT_TOKEN
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.api_integration import ApiIntegration
from integration_tests.utils.auth import Auth
from integration_tests.utils.orders import Orders

url_codes = f"{HOST}/api/v2/cml/codes"
url_utilisation = f"{HOST}/api/v2/cml/utilisation"


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
