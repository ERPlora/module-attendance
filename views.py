"""
Attendance & Clock-in Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('attendance', 'dashboard')
@htmx_view('attendance/pages/dashboard.html', 'attendance/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('attendance', 'records')
@htmx_view('attendance/pages/records.html', 'attendance/partials/records_content.html')
def records(request):
    """Records view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('attendance', 'settings')
@htmx_view('attendance/pages/settings.html', 'attendance/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

