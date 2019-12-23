class OrderDtoLight:
    @staticmethod
    def OrderDtoLight(contactPerson, contractDate, contractNumber, createMethodType, productionOrderId,
                 products, releaseMethodType):
        OrderDtoLight = {
        "contactPerson": contactPerson,
        "contractDate": contractDate,
        "contractNumber": contractNumber,
        "createMethodType": createMethodType,
        "productionOrderId": productionOrderId,
        "products": products,
        "releaseMethodType": releaseMethodType}
        return OrderDtoLight


