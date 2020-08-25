import uuid as uuid

from django.db import models

from communication.schedules.enums import CommunicationEnum, ScheduleStatusEnum


class Communication(models.Model):
    description = models.CharField(
        max_length=CommunicationEnum.get_database_max_length(),
        choices=CommunicationEnum.get_database_choices()
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.description}'


class Schedule(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    recipient = models.CharField(max_length=30)
    reservation = models.DateTimeField()
    communication = models.ForeignKey(
        'schedules.Communication',
        on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=ScheduleStatusEnum.get_database_max_length(),
        choices=ScheduleStatusEnum.get_database_choices(),
        default=ScheduleStatusEnum.SCHEDULED.value
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.uuid} - {self.message} - {self.created_at}'
