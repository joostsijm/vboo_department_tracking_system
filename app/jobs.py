"""Jobs for scheduler module"""

from app import app


def update_department(state_id, department_type):
    """Update department"""
    app.update_department(state_id, department_type)

def send_progress_message(state_id, department_type, language):
    """Send department progress message"""
    app.send_progress_message(state_id, department_type, language)
