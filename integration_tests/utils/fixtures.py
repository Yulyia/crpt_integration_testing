import pytest

from integration_tests.utils.contractor import Contractor


@pytest.fixture
def contractor_id():
    code, data = Contractor.get_contractor()
    return data['contractorId']
