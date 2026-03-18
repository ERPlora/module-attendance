from django.utils.translation import gettext_lazy as _

MODULE_ID = 'attendance'
MODULE_NAME = _('Attendance & Clock-in')
MODULE_VERSION = '1.0.1'
MODULE_ICON = 'material:schedule'
MODULE_DESCRIPTION = _('Employee attendance tracking and clock-in/out')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'hr'

MENU = {
    'label': _('Attendance & Clock-in'),
    'icon': 'time-outline',
    'order': 40,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Records'), 'icon': 'time-outline', 'id': 'records'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'attendance.view_attendancerecord',
'attendance.add_attendancerecord',
'attendance.change_attendancerecord',
'attendance.delete_attendancerecord',
'attendance.manage_settings',
]

ROLE_PERMISSIONS = {
    "admin": ["*"],
    "manager": [
        "add_attendancerecord",
        "change_attendancerecord",
        "view_attendancerecord",
    ],
    "employee": [
        "add_attendancerecord",
        "view_attendancerecord",
    ],
}
