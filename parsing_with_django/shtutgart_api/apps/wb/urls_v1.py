from django.urls import path
from apps.wb.views import *


urlpatterns = [
    path('product/', GetProductInfView.as_view()),
    path('catalog/', CatalogListView.as_view()),

]