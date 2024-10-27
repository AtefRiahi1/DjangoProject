from django.urls import path
from consommationEau.views import *

urlpatterns = [
    path('consommationEaus/', consommationEauFrontPage, name='consommationEauFrontPage'),
    path('consommationEau/details/<int:id>/', consommationEauDetail, name='consommationEauDetail'),
    path('consommationeau/create', consommationEauCreate, name='consommationEauCreate'),
    path('consommationeau/edit/<int:id>', consommationEauEdit, name='consommationEauEdit'),
    path('consommationeau/delete/<int:id>', consommationEauDelete, name='consommationEauDelete'),
    path('consommationeau/prediction_mensuelle', show_prediction, name='show_prediction'),
]