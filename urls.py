from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('records/', views.attendance_records_list, name='records'),


    # AttendanceRecord
    path('attendance_records/', views.attendance_records_list, name='attendance_records_list'),
    path('attendance_records/add/', views.attendance_record_add, name='attendance_record_add'),
    path('attendance_records/<uuid:pk>/edit/', views.attendance_record_edit, name='attendance_record_edit'),
    path('attendance_records/<uuid:pk>/delete/', views.attendance_record_delete, name='attendance_record_delete'),
    path('attendance_records/bulk/', views.attendance_records_bulk_action, name='attendance_records_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
