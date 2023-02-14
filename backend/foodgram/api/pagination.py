from rest_framework.pagination import LimitOffsetPagination


class SixItemPagination(LimitOffsetPagination):
    default_limit = 6
