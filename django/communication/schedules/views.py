from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from communication.schedules.models import Schedule
from communication.schedules.paginations import SchedulePagination
from communication.schedules.serializers import ScheduleSerializer

communications = settings.COMMUNICATION_LIST


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    ordering_fields = 'created'
    serializer_class = ScheduleSerializer
    pagination_class = SchedulePagination

    def create(self, request, *args, **kwargs):
        if request.data['communication'] not in communications:
            raise ValidationError(
                {'detail': f'communication not valid, fill one option in {communications}'},
                code=400
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
