
from rest_framework.pagination import PageNumberPagination


class DevicePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'device_page_size'
    max_page_size = 100