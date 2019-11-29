class OrderDtoProduct:
    @staticmethod
    def OrderDtoProduct(gtin, quantity, serialNumberType, template_id, serialNumbers=None):
        product = {
            "gtin" : gtin,
            "quantity" : quantity,
        "serialNumberType" : serialNumberType,
        "serialNumbers" : serialNumbers,
        "templateId" : template_id}
        return product
