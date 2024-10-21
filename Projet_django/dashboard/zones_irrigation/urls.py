from django.urls import path
from . import views

urlpatterns = [
    path('zones/index/', views.zone_list, name='zone_list'),  # Liste des zones
    path('zones/<int:id>/', views.zone_detail, name='zone_detail'),  # Détails d'une zone
    path('zones/create/', views.zone_create, name='zone_create'),  # Créer une zone
    path('zones/update/<int:id>/', views.zone_update, name='zone_update'),  # Modifier une zone
    path('zones/delete/<int:id>/', views.zone_delete, name='zone_delete'),  # Supprimer une zone
    path('zones/water-need-prediction/', views.water_need_prediction, name='water_need_prediction'),
]
