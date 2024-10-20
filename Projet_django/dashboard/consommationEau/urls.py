from django.urls import path
from consommationEau.views import *

urlpatterns = [
    path('consommationEaus/', consommationEauFrontPage, name='consommationEauFrontPage'),
    path('consommationEau/details/<int:id>/', consommationEauDetail, name='consommationEauDetail'),
]