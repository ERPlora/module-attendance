# Attendance & Clock-in Module

Employee attendance tracking and clock-in/out.

## Features

- Employee clock-in and clock-out recording
- Attendance statuses: Present, Late, Absent, Half Day, Remote
- Break time tracking in minutes
- Automatic total hours calculation
- Per-employee attendance history with notes
- Employee identification by ID and name

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Attendance & Clock-in > Settings**

## Usage

Access via: **Menu > Attendance & Clock-in**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/attendance/dashboard/` | Overview of today's attendance and statistics |
| Records | `/m/attendance/records/` | Browse and manage attendance records |
| Settings | `/m/attendance/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `AttendanceRecord` | Attendance entry with employee, clock-in/out times, break minutes, total hours, and status |

## Permissions

| Permission | Description |
|------------|-------------|
| `attendance.view_attendancerecord` | View attendance records |
| `attendance.add_attendancerecord` | Create attendance records |
| `attendance.change_attendancerecord` | Edit attendance records |
| `attendance.delete_attendancerecord` | Delete attendance records |
| `attendance.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
