"""Main app"""

import time

from app import scheduler, LOGGER
from app.api import get_professors
from app.database import get_latest_professor, save_professors


def job_update_department(state_id, department_type):
    """Update department professors"""
    LOGGER.info('"%s": Run update for "%s" department for state', state_id, department_type)
    latest_professor = get_latest_professor(state_id, department_type)
    date = None
    if latest_professor:
        date = latest_professor.date_time
    professors = get_professors(state_id, department_type, date)
    LOGGER.info(
        '"%s": Found "%s" new professors in "%s" department',
        state_id, len(professors), department_type
    )
    # print_professors(professors)
    save_professors(state_id, department_type, professors)
    LOGGER.info('"%s": saved professors', state_id)

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
    # job_update_department(2788, 2)
    # VN
    # uranium
    add_update_department(2788, 6)
    # gold
    add_update_department(2788, 2)
    # construction
    add_update_department(2788, 1)
    # oil
    add_update_department(2788, 3)
    # Belgium
    # gold
    add_update_department(2604, 2)
    # De Provincien
    # gold
    add_update_department(2620, 2)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print('Exiting application')
        exit()
