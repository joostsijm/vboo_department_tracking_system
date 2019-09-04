"""Main app"""

import time

from app import scheduler, session
from app.api import get_professors
from app.database import get_latest_professor, save_professors


def job_update_department(state_id, department_type):
    """Update department professors"""
    latest_professor = get_latest_professor(state_id, department_type)
    date = None
    if latest_professor:
        date = latest_professor.date_time
    professors = get_professors(state_id, department_type, date)
    print_professors(professors)
    save_professors(state_id, department_type, professors)

def print_professors(professors):
    """Print professors"""
    for professor in professors:
        print('{:30} {:2} {:>25}'.format(
            professor['name'],
            professor['points'],
            professor['date_time'].strftime('%d %B %Y %H:%M'),
        ))

def add_update_department(state_id, department_type):
    """Add jobs"""
    scheduler.add_job(
        job_update_department,
        'cron',
        args=[state_id, department_type],
        id='{}_{}'.format(state_id, department_type),
        replace_existing=True,
        hour='20'
    )

if __name__ == '__main__':
    # jobs
    # job_update_department(2788, 6)
    # VN
    # uranium
    job_update_department(2788, 6)
    # gold
    job_update_department(2788, 2)
    # construction
    job_update_department(2788, 1)
    # oil
    job_update_department(2788, 3)
    # Belgium
    # gold
    job_update_department(2604, 2)
    # De Provincien
    # gold
    job_update_department(2620, 2)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print('Exiting application')
        session.close()
        exit()
