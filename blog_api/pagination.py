from rest_framework.pagination import PageNumberPagination

__author__ = 'jaklimoff'


class PostsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
