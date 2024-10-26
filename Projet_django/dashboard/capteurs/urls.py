# capteurs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.sensor_list, name='sensor_list'),              # Read all sensors
    path('create/', views.sensor_create, name='sensor_create'),   # Create a sensor
    path('update/<int:pk>/', views.sensor_update, name='sensor_update'),  # Update sensor
    path('delete/<int:pk>/', views.sensor_delete, name='sensor_delete'),  # Delete sensor
    path('<int:capteur_id>/mesures/', views.mesure_list, name='mesure_list'),
    path('<int:capteur_id>/mesures/create/', views.mesure_create, name='mesure_create'),
    path('mesures/<int:mesure_id>/delete/', views.mesure_delete, name='mesure_delete'),
]
