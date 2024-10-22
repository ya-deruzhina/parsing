from rest_framework import generics
from rest_framework import pagination

from apps.wb.models import ProductModel
from apps.wb.serializers import CatalogSerializer    

class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20

class CatalogListView(generics.ListAPIView):
    serializer_class = CatalogSerializer
    pagination_class = DefaultPagination
    queryset = ProductModel.objects.all()