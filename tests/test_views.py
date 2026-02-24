"""Tests for attendance views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('attendance:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('attendance:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('attendance:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestAttendanceRecordViews:
    """AttendanceRecord view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('attendance:attendance_records_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('attendance:attendance_records_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('attendance:attendance_records_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('attendance:attendance_records_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('attendance:attendance_records_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('attendance:attendance_records_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('attendance:attendance_record_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('attendance:attendance_record_add')
        data = {
            'employee_id': 'test',
            'employee_name': 'New Employee Name',
            'clock_in': '2025-01-15T10:00',
            'clock_out': '2025-01-15T10:00',
            'break_minutes': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, attendance_record):
        """Test edit form loads."""
        url = reverse('attendance:attendance_record_edit', args=[attendance_record.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, attendance_record):
        """Test editing via POST."""
        url = reverse('attendance:attendance_record_edit', args=[attendance_record.pk])
        data = {
            'employee_id': 'test',
            'employee_name': 'Updated Employee Name',
            'clock_in': '2025-01-15T10:00',
            'clock_out': '2025-01-15T10:00',
            'break_minutes': '5',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, attendance_record):
        """Test soft delete via POST."""
        url = reverse('attendance:attendance_record_delete', args=[attendance_record.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        attendance_record.refresh_from_db()
        assert attendance_record.is_deleted is True

    def test_bulk_delete(self, auth_client, attendance_record):
        """Test bulk delete."""
        url = reverse('attendance:attendance_records_bulk_action')
        response = auth_client.post(url, {'ids': str(attendance_record.pk), 'action': 'delete'})
        assert response.status_code == 200
        attendance_record.refresh_from_db()
        assert attendance_record.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('attendance:attendance_records_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('attendance:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('attendance:settings')
        response = client.get(url)
        assert response.status_code == 302

