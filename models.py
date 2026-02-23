from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

ATT_STATUS = [
    ('present', _('Present')),
    ('late', _('Late')),
    ('absent', _('Absent')),
    ('half_day', _('Half Day')),
    ('remote', _('Remote')),
]

class AttendanceRecord(HubBaseModel):
    employee_id = models.UUIDField(db_index=True, verbose_name=_('Employee Id'))
    employee_name = models.CharField(max_length=255, verbose_name=_('Employee Name'))
    clock_in = models.DateTimeField(verbose_name=_('Clock In'))
    clock_out = models.DateTimeField(null=True, blank=True, verbose_name=_('Clock Out'))
    break_minutes = models.PositiveIntegerField(default=0, verbose_name=_('Break Minutes'))
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, default='0', verbose_name=_('Total Hours'))
    status = models.CharField(max_length=20, default='present', choices=ATT_STATUS, verbose_name=_('Status'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    class Meta(HubBaseModel.Meta):
        db_table = 'attendance_attendancerecord'

    def __str__(self):
        return str(self.id)

