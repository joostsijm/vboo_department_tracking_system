"""Main app"""

from datetime import datetime, timedelta
import random
import time

from app import scheduler
from app.api import get_professors
from app.database import get_latest_professor, save_professors


def job_update_department(state_id, department_type):
    """Update department professors"""
    # last_professor = get_last_professor(state_id, department_type)
    professors = get_professors(state_id, department_type, None)
    print_professors(professors)
    # save_professors(state_id, department_type, professors)

def print_professors(professors):
    """Print professors"""
    for professor in professors:
        print('{:30} {:2} {:>25}'.format(
            professor['name'],
            professor['points'],
            professor['date'].strftime('%d %B %Y %H:%M'),
        ))


if __name__ == '__main__':
    # jobs
    job_update_department(2788, 6)
    scheduler.add_job(
        job_update_department,
        'cron',
        args=[2788, 6],
        id='vn_update_department',
        replace_existing=True,
        hour='20'
    )

    while True:
        time.sleep(100)
