import pytest
from django.urls import reverse, NoReverseMatch
from model_bakery import baker
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient

from communication.schedules.models import Schedule

client = APIClient()
ERROR_NOT_FOUND = ErrorDetail(string='Not found.', code='not_found')
ERROR_MESSAGE_DATE = [
    ErrorDetail(
        string=f'Datetime has wrong format. Use one of these formats instead:'
               f' YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z].',
        code='invalid'
    )
]

ERROR_MESSAGE_COMMUNICATION = f'communication not valid, fill one option in' \
                              f' [\'sms\', \'email\', \'whatsapp\', \'push\']'


@pytest.mark.django_db
class TestSchedule:
    @pytest.fixture
    def schedule(self, communications):
        return baker.make(
            'schedules.Schedule',
            message="test message",
            recipient="xpto",
            reservation="2020-08-01 08:00:00",
            communication=communications[0]
        )

    def test_retrieve_schedule_and_does_not_exits(self):
        response = client.get(
            path=reverse(
                'schedule-details',
                args=['546901e9-0a0d-4d33-a39e-45b92820e087']
            ),
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_retrieve_schedule(self, schedule):
        response = client.get(
            path=reverse(
                'schedule-details',
                args=[schedule.uuid]
            ),
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

    def test_retrieve_schedule_should_not_exists(self):
        response = client.get(
            path=reverse(
                'schedule-details',
                args=['0e86382f-2765-4482-99b7-99caa31a7d43']
            ),
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == ERROR_NOT_FOUND

    def test_retrieve_schedule_with_no_uuid_patterns(self):
        with pytest.raises(NoReverseMatch):
            client.get(
                path=reverse(
                    'schedule-details',
                    args=['abcdefg']
                ),
                format='json'
            )

    @pytest.mark.parametrize(
        'message, recipient, reservation, communication', [
            ('message 1', 'mario', '2020-01-01 15:00:00', 'email'),
            ('message 1', 'joao', '2020-02-01 12:00:00', 'sms'),
            ('message 1', 'lara', '2020-03-01 17:00:00', 'push'),
            ('message 1', 'maria', '2020-04-01 19:00:00', 'whatsapp'),
        ]
    )
    def test_create_schedule(
        self,
        communications,
        message,
        recipient,
        reservation,
        communication
    ):
        response = client.post(
            path=reverse('create_schedule'),
            data={
                "message": message,
                "recipient": recipient,
                "reservation": reservation,
                "communication": communication
            },
            format='json'
        )
        schedules = Schedule.objects.all()

        assert response.status_code == status.HTTP_201_CREATED
        assert schedules

    @pytest.mark.parametrize(
        'message, recipient, reservation, communication, error_message', [
            ('message 1', 'mario', '2020-01-01 15:00:00', 'emailx', ERROR_MESSAGE_COMMUNICATION),
            ('message 1', 'joao', '2020-02-01 12:00:00', 'sMs', ERROR_MESSAGE_COMMUNICATION),
            ('message 1', 'maria', '2020-04-01 19:00:00', '', ERROR_MESSAGE_COMMUNICATION),
        ]
    )
    def test_create_schedule_with_invalid_data_should_return_exception(
        self,
        communications,
        message,
        recipient,
        reservation,
        communication,
        error_message
    ):
        response = client.post(
            path=reverse('create_schedule'),
            data={
                "message": message,
                "recipient": recipient,
                "reservation": reservation,
                "communication": communication
            },
            format='json'
        )
        schedules = Schedule.objects.all()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not schedules
        assert response.data['detail'] == error_message

    def test_create_schedule_with_invalid_datetime_should_return_exception(
        self,
        communications
    ):
        response = client.post(
            path=reverse('create_schedule'),
            data={
                "message": 'message 1',
                "recipient": 'lara',
                "reservation": '2020-03-01',
                "communication": 'push'
            },
            format='json'
        )
        schedules = Schedule.objects.all()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert not schedules
        assert response.data['reservation'] == ERROR_MESSAGE_DATE

    def test_delete_schedule(self, schedule):
        response = client.delete(
            path=reverse(
                'schedule-details',
                args=[schedule.uuid]
            ),
            format='json'
        )
        schedules = Schedule.objects.all()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not schedules

    def test_delete_schedule_should_not_exists(self):
        response = client.delete(
            path=reverse(
                'schedule-details',
                args=['0e86382f-2765-4482-99b7-99caa31a7d43']
            ),
            format='json'
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data['detail'] == ERROR_NOT_FOUND
