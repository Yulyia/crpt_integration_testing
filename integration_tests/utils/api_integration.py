
class ApiIntegration:

    @staticmethod
    def post_aggregation(data_codes, aggregation_type, quality):
        data_aggregation = {
            "aggregationUnits": [
                {
                    "aggregatedItemsCount": 2,
                    "aggregationType": aggregation_type,
                    "aggregationUnitCapacity": 10,
                    "sntins": [{
                                   "code": data_codes['codes'][0],
                                   "quality": quality[0]},
                               {
                                   "code": data_codes['codes'][1],
                                   "quality": quality[1]}],
                    "unitSerialNumber": "String"
                }]}
        return data_aggregation

    @staticmethod
    def post_utilisation(data_codes, usage_type):
        data_utilisation = {
                "sntins": [
                    data_codes['codes'][0],
                    data_codes['codes'][1],
                    ],
                "usageType": usage_type
            }
        return data_utilisation
