from integration_tests.utils.api_helpers import ClientApi
from integration_tests.constants import HOST


report_url_in_kd = f"{HOST}/webapi/v1/reports"
params = {"limit": 10, "skip": 0, "total": 0, "sort": ""}


class Report:
    @staticmethod
    def get_report_id(jsessionid):
        api = ClientApi()
        code, data = api.get(url=report_url_in_kd, params=params, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        report_id = data['result'][0]['id']
        return report_id

