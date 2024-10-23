from django.urls import path
from . import views

urlpatterns = [
    path('myplans/', views.irrigation_plan_list, name='irrigation_plan_list'),  #
    path('create/', views.irrigation_plan_create, name='irrigation_plan_create'), 
    path('update/<int:pk>/', views.irrigation_plan_update, name='irrigation_plan_update'), 
    path('deleteplan/<int:pk>/', views.irrigation_plan_delete, name='irrigation_plan_delete'),
    path('apiplans/', views.irrigation_plans_view, name='irrigation-plans'),

]
