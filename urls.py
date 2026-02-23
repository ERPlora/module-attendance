from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('records/', views.records, name='records'),
    path('settings/', views.settings, name='settings'),
]
