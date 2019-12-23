from integration_tests.constants import STAND_KD
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.auth import Auth

url_get_contractors = f"{STAND_KD}/webapi/v1/contractor"


class Contractor:
    @staticmethod
    def get_contractor():
        jsessionid = Auth.get_jssesion_id()
        api = ClientApi()
        code, data = api.get(url=url_get_contractors, headers={"Cookie": f"JSESSIONID={jsessionid}"})
        return code, data

