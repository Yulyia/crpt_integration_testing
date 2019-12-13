from integration_tests.constants import HOST, HOST_SUZ
from integration_tests.utils.api_helpers import ClientApi
from integration_tests.utils.get_order_dto_light import OrderLights, OrderProductPharma, OrderProductTobacco, \
    OrderProductMilk



contractorId = "e6b93cf3-e336-4f9e-946c-0d3abd6378d8"
clientToken = "1cecc8fb-fb47-4c8a-af3d-d34c1ead8c4f"

QUANTITY = 50


GTIN_SHOES = ["04616052543059", "04630034070012", "04650117240200"]
GTIN_PHARMA = "88833355588800"
GTIN_TOBACCO = "05995327112039"
GTIN_MILK = "04607070190028"
URL_GET_ORDERS_LIGHT = HOST_SUZ + "/api/v2/light/orders"
URL_GET_ORDERS_PHARMA = HOST_SUZ + "/api/v2/pharma/orders"
URL_GET_ORDERS_TOBACCO = HOST_SUZ + "/api/v2/tobacco/orders"
URL_GET_ORDERS_MILK = HOST_SUZ + "/api/v2/milk/orders"


def test_get_orders_light_for_contractor():
    quantity = QUANTITY
    SHOES_TEMPLATE = 1
    api = ClientApi()
    request = OrderLights.get_order_dto_light_request(GTIN_SHOES, quantity, SHOES_TEMPLATE)
    param = {'omsId': contractorId}
    headers = {'clientToken': clientToken}
    code, data = api.post(url=URL_GET_ORDERS_LIGHT, headers=headers, params=param,
                          json=request, verify=False)
    assert code == 200


def test_get_orders_pharma_for_contractor():
    quantity = QUANTITY
    api = ClientApi()
    request = OrderProductPharma.get_order_for_pharma_request(GTIN_PHARMA, quantity)
    param = {'omsId': contractorId}
    headers = {'clientToken': clientToken}
    code, data = api.post(url=URL_GET_ORDERS_PHARMA, headers=headers, params=param,
                          json=request, verify=False)
    assert code == 200


def test_get_orders_tobacco_for_contractor():
    quantity = QUANTITY
    api = ClientApi()
    request = OrderProductTobacco.get_order_for_tobacco_request(GTIN_TOBACCO, quantity)
    param = {'omsId': contractorId}
    headers = {'clientToken': clientToken}
    code, data = api.post(url=URL_GET_ORDERS_TOBACCO, headers=headers, params=param,
                          json=request, verify=False)
    assert code == 200


# def test_get_orders_milk_for_contractor():
#     quantity = QUANTITY
#     api = ClientApi()
#     request = OrderProductMilk.get_order_for_milk_request(GTIN_MILK, quantity)
#     param = {'omsId': contractorId}
#     headers = {'clientToken': clientToken}
#     code, data = api.post(url=URL_GET_ORDERS_MILK, headers=headers, params=param,
#                           json=request, verify=False)
#     assert code == 200

