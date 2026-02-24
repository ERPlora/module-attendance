from django.contrib import admin

from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'employee_name', 'clock_in', 'clock_out', 'break_minutes', 'created_at']
    search_fields = ['employee_name', 'status', 'notes']
    readonly_fields = ['created_at', 'updated_at']

