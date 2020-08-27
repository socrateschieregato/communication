import pytest
from model_bakery import baker


@pytest.fixture
def communications():
    communication_list = ['email', 'sms', 'push', 'whatsapp']
    communications = []
    for communication in communication_list:
        communications.append(
            baker.make(
                'schedules.Communication',
                description=communication
            )
        )
    return communications
