"""Scheduled task handlers for attendance module."""
import logging
logger = logging.getLogger(__name__)

def generate_monthly_report(payload):
    """Aggregate attendance data and generate monthly report."""
    logger.info('attendance.generate_monthly_report called')
    return {'status': 'not_implemented'}
