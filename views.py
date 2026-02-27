"""
Attendance & Clock-in Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import AttendanceRecord

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('attendance', 'dashboard')
@htmx_view('attendance/pages/index.html', 'attendance/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_attendance_records': AttendanceRecord.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# AttendanceRecord
# ======================================================================

ATTENDANCE_RECORD_SORT_FIELDS = {
    'status': 'status',
    'total_hours': 'total_hours',
    'break_minutes': 'break_minutes',
    'employee_id': 'employee_id',
    'employee_name': 'employee_name',
    'clock_in': 'clock_in',
    'created_at': 'created_at',
}

def _build_attendance_records_context(hub_id, per_page=10):
    qs = AttendanceRecord.objects.filter(hub_id=hub_id, is_deleted=False).order_by('status')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'attendance_records': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'status',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_attendance_records_list(request, hub_id, per_page=10):
    ctx = _build_attendance_records_context(hub_id, per_page)
    return django_render(request, 'attendance/partials/attendance_records_list.html', ctx)

@login_required
@with_module_nav('attendance', 'records')
@htmx_view('attendance/pages/attendance_records.html', 'attendance/partials/attendance_records_content.html')
def attendance_records_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'status')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = AttendanceRecord.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(employee_name__icontains=search_query) | Q(status__icontains=search_query) | Q(notes__icontains=search_query))

    order_by = ATTENDANCE_RECORD_SORT_FIELDS.get(sort_field, 'status')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['status', 'total_hours', 'break_minutes', 'employee_id', 'employee_name', 'clock_in']
        headers = ['Status', 'Total Hours', 'Break Minutes', 'Employee Id', 'Employee Name', 'Clock In']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='attendance_records.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='attendance_records.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'attendance/partials/attendance_records_list.html', {
            'attendance_records': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'attendance_records': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def attendance_record_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id', '').strip()
        employee_name = request.POST.get('employee_name', '').strip()
        clock_in = request.POST.get('clock_in') or None
        clock_out = request.POST.get('clock_out') or None
        break_minutes = int(request.POST.get('break_minutes', 0) or 0)
        total_hours = request.POST.get('total_hours', '0') or '0'
        status = request.POST.get('status', '').strip()
        notes = request.POST.get('notes', '').strip()
        obj = AttendanceRecord(hub_id=hub_id)
        obj.employee_id = employee_id
        obj.employee_name = employee_name
        obj.clock_in = clock_in
        obj.clock_out = clock_out
        obj.break_minutes = break_minutes
        obj.total_hours = total_hours
        obj.status = status
        obj.notes = notes
        obj.save()
        return _render_attendance_records_list(request, hub_id)
    return django_render(request, 'attendance/partials/panel_attendance_record_add.html', {})

@login_required
def attendance_record_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(AttendanceRecord, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.employee_id = request.POST.get('employee_id', '').strip()
        obj.employee_name = request.POST.get('employee_name', '').strip()
        obj.clock_in = request.POST.get('clock_in') or None
        obj.clock_out = request.POST.get('clock_out') or None
        obj.break_minutes = int(request.POST.get('break_minutes', 0) or 0)
        obj.total_hours = request.POST.get('total_hours', '0') or '0'
        obj.status = request.POST.get('status', '').strip()
        obj.notes = request.POST.get('notes', '').strip()
        obj.save()
        return _render_attendance_records_list(request, hub_id)
    return django_render(request, 'attendance/partials/panel_attendance_record_edit.html', {'obj': obj})

@login_required
@require_POST
def attendance_record_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(AttendanceRecord, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_attendance_records_list(request, hub_id)

@login_required
@require_POST
def attendance_records_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = AttendanceRecord.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_attendance_records_list(request, hub_id)


@login_required
@permission_required('attendance.manage_settings')
@with_module_nav('attendance', 'settings')
@htmx_view('attendance/pages/settings.html', 'attendance/partials/settings_content.html')
def settings_view(request):
    return {}

