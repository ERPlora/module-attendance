"""
AI context for the Attendance module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Attendance

### Models

**AttendanceRecord**
- employee_id (UUID, indexed) — references the employee's UUID
- employee_name (str, cached for display)
- clock_in (DateTimeField) — when the employee arrived
- clock_out (DateTimeField, optional) — when the employee left; null if still clocked in
- break_minutes (int, default 0) — total break time in minutes
- total_hours (Decimal) — net worked hours (must be calculated before saving)
- status: present | late | absent | half_day | remote
- notes (text)

### Key flows

1. **Record arrival**: Create AttendanceRecord with employee_id, clock_in datetime, status (present/late/remote)
2. **Record departure**: Update clock_out on the open record; set total_hours = (clock_out - clock_in - break_minutes)
3. **Mark absent**: Create record with status=absent, no clock_in/clock_out required
4. **Query today's attendance**: Filter by clock_in__date=today

### Notes

- employee_id is a UUID matching the staff member's pk (no FK enforced)
- total_hours is not auto-computed — caller must calculate and set it
- A record with clock_out=null means the employee is currently clocked in
- For legal clock-in/clock-out tracking with geolocation, use the time_control module instead
"""
