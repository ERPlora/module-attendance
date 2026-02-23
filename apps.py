from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendance'
    label = 'attendance'
    verbose_name = _('Attendance & Clock-in')

    def ready(self):
        pass
