from rest_framework.pagination import LimitOffsetPagination


class SchedulePagination(LimitOffsetPagination):
    default_limit = 10
