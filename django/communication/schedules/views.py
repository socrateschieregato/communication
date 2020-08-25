from rest_framework import viewsets

from communication.schedules.models import Schedule
from communication.schedules.paginations import SchedulePagination
from communication.schedules.serializers import ScheduleSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    ordering_fields = 'created'
    serializer_class = ScheduleSerializer
    pagination_class = SchedulePagination
