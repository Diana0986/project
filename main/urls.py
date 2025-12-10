from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.popular_list, name='popular_list'),
    path('news/', views.new_list, name='new_list'),
    path('news/<slug:slug>/', views.new_detail,
         name='new_detail'),
    path('events/', views.events_list, name='events_list'),
    path('clubs/', views.clubs_list, name='clubs_list'),
    path('services/', views.services_list, name='services_list'),
    path('supports/', views.support_list, name='support_list'),
    path('supports/initiative-form/', views.initiative_form, name='initiative_form'),
]
