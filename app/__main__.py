"""Main app"""

import sys
import time

from app import SCHEDULER, LOGGER, jobs, job_storage


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
    SCHEDULER.add_job(
        jobs.update_department,
        'cron',
        args=[state_id, department_type],
        id='{}_{}'.format(state_id, department_type),
        replace_existing=True,
        hour='19'
    )

def add_send_progress_message(state_id, department_type, language):
    """Add send_message"""
    SCHEDULER.add_job(
        jobs.send_progress_message,
        'cron',
        args=[state_id, department_type, language],
        id='send_progress_message_{}_{}'.format(state_id, department_type),
        replace_existing=True,
        hour='19',
        minute='10'
    )

def add_send_lotery_message(state_id, department_type, language, amount):
    """Add send_message"""
    SCHEDULER.add_job(
        jobs.send_lotery_message,
        'cron',
        args=[state_id, department_type, language, amount],
        id='send_loter_message_{}_{}'.format(state_id, department_type),
        replace_existing=True,
        hour='8',
    )

if __name__ == '__main__':
    # jobs
    # jobs.update_department(2788, 6)
    # jobs.send_progress_message(2788, 6, 'nl')
    # jobs.send_lotery_message(2788, 6, 'nl', 1e9)
    # sys.exit()

    # Jobs
    JOBS = job_storage.get_jobs()
    for job in JOBS:
        LOGGER.info(
            'For "%s" add department "%s" update',
            job['state_id'],
            job['department_type']
        )
        SCHEDULER.add_job(
            jobs.update_department,
            'cron',
            args=[job['state_id'], job['department_type']],
            id='{}_{}'.format(job['state_id'], job['department_type']),
            replace_existing=True,
            hour='19'
        )

    # progress message VN uranium
    add_send_progress_message(2788, 6, 'nl')
    add_send_lotery_message(2788, 6, 'nl', 36e8)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print('Exiting application')
        SCHEDULER.shutdown()
        sys.exit()
