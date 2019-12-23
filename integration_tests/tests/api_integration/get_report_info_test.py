import logging

from integration_tests.constants import CLIENT_TOKEN_KD, STAND_KD
from integration_tests.example_response.report_info import response_report_info
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.auth import Auth
from integration_tests.utils.report import Report

url_report_info = f"{STAND_KD}/api/v2/cml/report/info"


def test_positive_report_info():
    logging.info(f"Проверка позитивного сценария выполнения запроса {url_report_info}")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    report_id = Report.get_report_id(jsessionid)
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url_report_info, headers=headers, params={"reportId": report_id})
    mismatch_keys = [key for key in data if key not in response_report_info]
    for key in mismatch_keys:
        logging.info(f' do not have key in response_orders: {key}')

    mismatch_keys1 = [key for key in response_report_info if key not in data]
    for key in mismatch_keys1:
        logging.info(f' do not have key in data: {key}')
    assert len(mismatch_keys) == 0 and len(mismatch_keys1) == 0
    assert code == 200


def test_negative_report_info_required_reportid():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_report_info}"
                 f" без обязательного параметра запроса reportId")
    api = ClientApi()
    headers = {"clientToken": CLIENT_TOKEN_KD}
    code, data = api.get(url_report_info, headers=headers)
    assert code == 400
    assert data['errorCode'] == 400 and data['errorText'] == 'Required String parameter \'reportId\' is not present'


def test_negative_report_info_required_client_token():
    logging.info(f"Проверка негативного сценария выполнения запроса {url_report_info}"
                 f" без токена")
    api = ClientApi()
    jsessionid = Auth.get_jssesion_id()
    report_id = Report.get_report_id(jsessionid)
    code, data = api.get(url_report_info, params={"reportId": report_id})
    assert code == 400
    assert data['errorCode'] == 400
    assert data['errorText'] == "Missing request header 'clientToken' for method parameter of type String"
    assert len(data) == 2