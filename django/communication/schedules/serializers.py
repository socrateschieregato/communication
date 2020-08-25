from rest_framework import serializers

from communication.schedules.models import Communication, Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    communication = serializers.SlugRelatedField(
        queryset=Communication.objects.all(),
        slug_field='description'
    )

    class Meta:
        model = Schedule
        fields = [
            'uuid',
            'message',
            'recipient',
            'reservation',
            'status',
            'updated_at',
            'created_at',
            'communication'
        ]
