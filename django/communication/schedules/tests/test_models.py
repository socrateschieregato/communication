from datetime import datetime

import pytest
import pytz
from model_bakery import baker

from communication.schedules.models import Schedule


@pytest.mark.django_db
class TestModelPackage:
    @pytest.fixture
    def reservation(self):
        return datetime(2020, 8, 25, 11, 14, 00, tzinfo=pytz.utc)

    @pytest.fixture
    def schedule(self, reservation, communications):
        return baker.make(
            'schedules.Schedule',
            message="test message",
            recipient="xpto",
            reservation=reservation,
            communication=communications[0]
        )

    def test_schedule_date(self, schedule):
        assert isinstance(schedule.created_at, datetime)
        assert isinstance(schedule.reservation, datetime)
        assert isinstance(schedule.updated_at, datetime)

    def test_schedule_model(self, reservation, communications):
        schedule = Schedule.objects.create(
            message="test message",
            recipient="xpto",
            reservation=reservation,
            communication=communications[0]
        )
        assert schedule
