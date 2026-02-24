"""Tests for attendance models."""
import pytest
from django.utils import timezone

from attendance.models import AttendanceRecord


@pytest.mark.django_db
class TestAttendanceRecord:
    """AttendanceRecord model tests."""

    def test_create(self, attendance_record):
        """Test AttendanceRecord creation."""
        assert attendance_record.pk is not None
        assert attendance_record.is_deleted is False

    def test_soft_delete(self, attendance_record):
        """Test soft delete."""
        pk = attendance_record.pk
        attendance_record.is_deleted = True
        attendance_record.deleted_at = timezone.now()
        attendance_record.save()
        assert not AttendanceRecord.objects.filter(pk=pk).exists()
        assert AttendanceRecord.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, attendance_record):
        """Test default queryset excludes deleted."""
        attendance_record.is_deleted = True
        attendance_record.deleted_at = timezone.now()
        attendance_record.save()
        assert AttendanceRecord.objects.filter(hub_id=hub_id).count() == 0


