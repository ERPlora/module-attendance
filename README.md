# Attendance & Clock-in

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `attendance` |
| **Version** | `1.0.0` |
| **Icon** | `time-outline` |
| **Dependencies** | None |

## Models

### `AttendanceRecord`

AttendanceRecord(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, employee_id, employee_name, clock_in, clock_out, break_minutes, total_hours, status, notes)

| Field | Type | Details |
|-------|------|---------|
| `employee_id` | UUIDField | max_length=32 |
| `employee_name` | CharField | max_length=255 |
| `clock_in` | DateTimeField |  |
| `clock_out` | DateTimeField | optional |
| `break_minutes` | PositiveIntegerField |  |
| `total_hours` | DecimalField |  |
| `status` | CharField | max_length=20, choices: present, late, absent, half_day, remote |
| `notes` | TextField | optional |

## URL Endpoints

Base path: `/m/attendance/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `records/` | `records` | GET |
| `attendance_records/` | `attendance_records_list` | GET |
| `attendance_records/add/` | `attendance_record_add` | GET/POST |
| `attendance_records/<uuid:pk>/edit/` | `attendance_record_edit` | GET |
| `attendance_records/<uuid:pk>/delete/` | `attendance_record_delete` | GET/POST |
| `attendance_records/bulk/` | `attendance_records_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `attendance.view_attendancerecord` | View Attendancerecord |
| `attendance.add_attendancerecord` | Add Attendancerecord |
| `attendance.change_attendancerecord` | Change Attendancerecord |
| `attendance.delete_attendancerecord` | Delete Attendancerecord |
| `attendance.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_attendancerecord`, `change_attendancerecord`, `view_attendancerecord`
- **employee**: `add_attendancerecord`, `view_attendancerecord`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Records | `time-outline` | `records` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_attendance_records`

List attendance records with filters.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `employee_id` | string | No |  |
| `status` | string | No | Filter: present, late, absent, half_day, remote |
| `date_from` | string | No |  |
| `date_to` | string | No |  |
| `limit` | integer | No |  |

### `create_attendance_record`

Create an attendance record (clock in).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `employee_id` | string | Yes |  |
| `employee_name` | string | Yes |  |
| `clock_in` | string | Yes | Clock in time (ISO format) |
| `status` | string | No | present, late, remote |
| `notes` | string | No |  |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  attendance/
    css/
    js/
  icons/
    icon.svg
templates/
  attendance/
    pages/
      attendance_record_add.html
      attendance_record_edit.html
      attendance_records.html
      dashboard.html
      index.html
      records.html
      settings.html
    partials/
      attendance_record_add_content.html
      attendance_record_edit_content.html
      attendance_records_content.html
      attendance_records_list.html
      dashboard_content.html
      panel_attendance_record_add.html
      panel_attendance_record_edit.html
      records_content.html
      settings_content.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
