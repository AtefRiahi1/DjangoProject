from django.urls import path
from consommationEau.views import *

urlpatterns = [
    path('consommationEaus/', consommationEauFrontPage, name='consommationEauFrontPage'),
    path('consommationEau/details/<int:id>/', consommationEauDetail, name='consommationEauDetail'),
    path('consommationeau/create', consommationEauCreate, name='consommationEauCreate'),
    path('consommationeau/edit/<int:id>', consommationEauEdit, name='consommationEauEdit'),
    path('consommationeau/delete/<int:id>', consommationEauDelete, name='consommationEauDelete'),
    path('consommationeau/prediction_mensuelle', show_prediction, name='show_prediction'),
    path('irrigations/', irrigationFrontPage, name='irrigationFrontPage'),

    # URL pour les détails d'une irrigation spécifique
    path('irrigations/<int:id>/', irrigationDetail, name='irrigationDetail'),

    # URL pour la création d'une nouvelle irrigation
    path('irrigations/create/', irrigationCreate, name='irrigationCreate'),

    # URL pour l'édition d'une irrigation existante
    path('irrigations/edit/<int:id>/', irrigationEdit, name='irrigationEdit'),

    # URL pour la suppression d'une irrigation
    path('irrigations/delete/<int:id>/', irrigationDelete, name='irrigationDelete'),
]