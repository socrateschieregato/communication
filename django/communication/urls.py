from django.contrib import admin
from django.urls import path

from communication.schedules.views import ScheduleViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'schedules/',
        ScheduleViewSet.as_view({'post': 'create'}),
        name='create_schedule'
    ),
    path(
        'schedules/<uuid:pk>/',
        ScheduleViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
        name='schedule-details'
    )
]
