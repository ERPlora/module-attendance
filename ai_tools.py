"""AI tools for the Attendance module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListAttendanceRecords(AssistantTool):
    name = "list_attendance_records"
    description = "List attendance records with filters."
    module_id = "attendance"
    required_permission = "attendance.view_attendancerecord"
    parameters = {
        "type": "object",
        "properties": {
            "employee_id": {"type": "string"},
            "status": {"type": "string", "description": "Filter: present, late, absent, half_day, remote"},
            "date_from": {"type": "string"}, "date_to": {"type": "string"},
            "limit": {"type": "integer"},
        },
        "required": [],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from attendance.models import AttendanceRecord
        qs = AttendanceRecord.objects.all()
        if args.get('employee_id'):
            qs = qs.filter(employee_id=args['employee_id'])
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('date_from'):
            qs = qs.filter(clock_in__date__gte=args['date_from'])
        if args.get('date_to'):
            qs = qs.filter(clock_in__date__lte=args['date_to'])
        limit = args.get('limit', 20)
        return {
            "records": [
                {
                    "id": str(r.id), "employee_name": r.employee_name, "status": r.status,
                    "clock_in": r.clock_in.isoformat() if r.clock_in else None,
                    "clock_out": r.clock_out.isoformat() if r.clock_out else None,
                    "total_hours": str(r.total_hours) if r.total_hours else None,
                    "break_minutes": r.break_minutes,
                }
                for r in qs.order_by('-clock_in')[:limit]
            ]
        }


@register_tool
class CreateAttendanceRecord(AssistantTool):
    name = "create_attendance_record"
    description = "Create an attendance record (clock in)."
    module_id = "attendance"
    required_permission = "attendance.add_attendancerecord"
    requires_confirmation = True
    parameters = {
        "type": "object",
        "properties": {
            "employee_id": {"type": "string"}, "employee_name": {"type": "string"},
            "clock_in": {"type": "string", "description": "Clock in time (ISO format)"},
            "status": {"type": "string", "description": "present, late, remote"},
            "notes": {"type": "string"},
        },
        "required": ["employee_id", "employee_name", "clock_in"],
        "additionalProperties": False,
    }

    def execute(self, args, request):
        from attendance.models import AttendanceRecord
        r = AttendanceRecord.objects.create(
            employee_id=args['employee_id'], employee_name=args['employee_name'],
            clock_in=args['clock_in'], status=args.get('status', 'present'),
            notes=args.get('notes', ''),
        )
        return {"id": str(r.id), "employee_name": r.employee_name, "created": True}
