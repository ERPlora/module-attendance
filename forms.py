from django import forms
from django.utils.translation import gettext_lazy as _

from .models import AttendanceRecord

class AttendanceRecordForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['employee_id', 'employee_name', 'clock_in', 'clock_out', 'break_minutes', 'total_hours', 'status', 'notes']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'employee_name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'clock_in': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'clock_out': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'break_minutes': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'total_hours': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'status': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'notes': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

