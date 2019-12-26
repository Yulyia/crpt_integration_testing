import logging

from integration_tests.utils.auth import Auth
from integration_tests.utils.report_kd_helper import Report


def test_positive_get_report():
    logging.info(f"Проверка позитивного сценария получения списка отчётов")
    jsessionid = Auth.get_jssesion_id()
    code, data = Report.get_report(jsessionid)
    assert code == 200
    assert data['result'][0]['status'] is not None


def test_positive_filter_by_type():
    logging.info(f"Проверка позитивного сценария получения списка отчётов отфильтрованного по типам")
    jsessionid = Auth.get_jssesion_id()
    code, data = Report.get_report_by_type(jsessionid, "AGGREGATION_REPORT")
    for report in data['result']:
        if report['type'] != "AGGREGATION_REPORT":
            logging.info(f"Фильтрация не работает, в фильтре на аггрегацию попал отчёт {report['type']}")
            assert False
    code, data = Report.get_report_by_type(jsessionid, "UTILISATION_REPORT")
    for report in data['result']:
        if report['type'] != "UTILISATION_REPORT":
            logging.info(f"Фильтрация не работает, в фильтре на аггрегацию попал отчёт {report['type']}")
            assert False
    code, data = Report.get_report_by_type(jsessionid, "DROPOUT_REPORT")
    for report in data['result']:
        if report['type'] != "DROPOUT_REPORT":
            logging.info(f"Фильтрация не работает, в фильтре на аггрегацию попал отчёт {report['type']}")
            assert False



