from django.urls import path
from . import views

urlpatterns = [
    path('myplans/', views.irrigation_plan_list, name='irrigation_plan_list'),  #
    path('create/', views.irrigation_plan_create, name='irrigation_plan_create'), 
    path('update/<int:pk>/', views.irrigation_plan_update, name='irrigation_plan_update'), 
    path('deleteplan/<int:pk>/', views.irrigation_plan_delete, name='irrigation_plan_delete'),
    path('apiplans/', views.irrigation_plans_view, name='irrigation-plans'),
    path('location-form/', views.location_form, name='location_form'),
    path('results/', views.results_view, name='results_page'),
    path('add-irrigation/', views.add_irrigation, name='add_irrigation'),
    #schedule
    path('myschedule/', views.irrigation_schedule_list, name='irrigation_schedule_list'), 
    path('schedules/create/', views.add_irrigation_schedule, name='irrigation_schedule_create'),  
    path('schedules/update/<int:pk>/', views.irrigation_schedule_update, name='irrigation_schedule_update'), 
    path('schedules/delete/<int:pk>/', views.irrigation_schedule_delete, name='irrigation_schedule_delete'),

]
