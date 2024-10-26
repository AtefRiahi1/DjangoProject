# capteurs/urls.py
from django.urls import path
from .views import sensor_list, sensor_create, sensor_update, sensor_delete

urlpatterns = [
    path('capteurs/index/', sensor_list, name='sensor_list'),              # Read all sensors
    path('capteurs/create/', sensor_create, name='sensor_create'),   # Create a sensor
    path('capteurs/update/<int:pk>/', sensor_update, name='sensor_update'),  # Update sensor
    path('capteurs/delete/<int:pk>/', sensor_delete, name='sensor_delete'),  # Delete sensor
]
