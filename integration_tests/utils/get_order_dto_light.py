from datetime import date, timedelta
from random import randint

import uuid

from integration_tests.types.OrdersDtoLight import OrderDtoLight


class OrderLights:
    @staticmethod
    def get_order_dto_light_request(gtin, quantity, template_id):
        products = []
        for i in range(len(gtin)):
            products.append({
                "gtin": gtin[i],
                "quantity": quantity,
                "serialNumberType": "OPERATOR",
                "serialNumbers": None,
                "templateId": 1})
        ContractDate = date.today() + timedelta(days=90)
        ContractNumber = str(randint(1000000000, 9999999999))
        uuid_ = uuid.uuid1()
        orders = OrderDtoLight.OrderDtoLight(contactPerson="Test", contractDate=str(ContractDate), contractNumber=ContractNumber,
                               createMethodType="SELF_MADE",
                               productionOrderId=str(uuid_), releaseMethodType="IMPORT", products=products)
        return orders


class OrderProductPharma:
    @staticmethod
    def get_order_for_pharma_request(gtin_, quantity):
        products = [
            {"gtin": gtin_,
             "quantity": quantity,
             "serialNumberType": "OPERATOR",
             "serialNumbers": None,
             "templateId": 2
             }]
        uuid_ = uuid.uuid4()
        orders = {
            "freeCode": False,
            "paymentType": 1,
            "products": products,
            "subjectId": str(uuid_)
        }
        return orders


class OrderProductTobacco:
    @staticmethod
    def get_order_for_tobacco_request(gtin_, quantity):
        products = [{
            "gtin": gtin_,
            "mrp": "100000",
            "quantity": quantity,
            "serialNumberType": "OPERATOR",
            "serialNumbers": None,
            "templateId": 3}]
        orders = {
            "expectedStartDate": str(date.today()),
            "factoryAddress":"ul. Pervaya Tabachnaya, 7",
            "factoryId": "ftf_001",
            "factoryName": "First Tobacco Factory",
            "poNumber": 123456,
            "productCode":"ABCD123456",
            "productDescription": "Cigarettes Friend",
            "productionLineId": 123,
            "products": products,
            "factoryCountry": "RU"
        }
        return orders


class OrderProductMilk:
    @staticmethod
    def get_order_for_milk_request(gtin_, quantity):
        products = [{
            "gtin": gtin_,
            "quantity": quantity,
            "serialNumberType": "OPERATOR",
            "serialNumbers": None,
            "templateId": 6}]
        orders = {
            "contactPerson": "John Smith (Иванов Петр Сидорович)",
            "contractDate": str(date.today()),
            "createMethodType": "CEM",
            "productionOrderId": str(uuid.uuid4()),
            "products": products,
            "releaseMethodType": "IMPORT"
        }
        return orders


class OrderProductWheelchairs:
    @staticmethod
    def get_order_for_wheelchairs_request(gtin, quantity):
        products = []
        for i in range(len(gtin)):
            products.append({
                "gtin": gtin[i],
                "quantity": quantity,
                "serialNumberType": "OPERATOR",
                "serialNumbers": None,
                "templateId": 12})

        contract_date = date.today() + timedelta(days=90)
        contract_number = str(randint(1000000000, 9999999999))
        uuid_ = uuid.uuid1()
        orders = OrderDtoLight.OrderDtoLight(contactPerson="Test", contractDate=str(contract_date),
                                             contractNumber=contract_number,
                                             createMethodType="SELF_MADE",
                                             productionOrderId=str(uuid_), releaseMethodType="IMPORT", products=products)
        return orders



