from datetime import date, timedelta
from random import randint

import uuid

from integration_tests.types.OrderDtoProduct import OrderDtoProduct
from integration_tests.types.OrdersDtoLight import OrderDtoLight


class OrderLights:
    @staticmethod
    def get_order_dto_light_request(gtin, quantity, template_id):
        products = [OrderDtoProduct.OrderDtoProduct(gtin, quantity, "OPERATOR", template_id)]
        ContractDate = date.today() + timedelta(days=90)
        ContractNumber = randint(1000000000, 9999999999)
        uuid_ = uuid.uuid1()
        orders = OrderDtoLight.OrderDtoLight(contactPerson="Test", contractDate=str(ContractDate), contractNumber=ContractNumber,
                               createMethodType="SELF_MADE",
                               productionOrderId=str(uuid_), releaseMethodType="IMPORT", products=products)
        return orders
