from integration_tests.utils.api_helpers import ClientApi
from integration_tests.constants import STAND_KD


report_url_in_kd = f"{STAND_KD}/webapi/v1/reports"



class Report:
    @staticmethod
    def get_report(jsessionid):
        api = ClientApi()
        params = {"limit": 10, "skip": 0, "total": 0, "sort": ""}
        code, data = api.get(url=report_url_in_kd, params=params, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data

    @staticmethod
    def get_report_by_type(jsessionid, type):
        api = ClientApi()
        params = {"limit": 50, "skip": 0, "total": 0, "sort": "", "type": type}
        code, data = api.get(url=report_url_in_kd, params=params, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data


