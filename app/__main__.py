"""Main app"""

import math
import time

from app import scheduler, LOGGER
from app.api import get_professors, get_institutes, send_message
from app.database import get_latest_professor, save_professors, get_yesterday_professors


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

def job_send_progress_message(state_id, department_type, language):
    """Update department professors"""
    LOGGER.info('"%s": Send progress message for "%s" department', state_id, department_type)
    yesterday_professors = get_yesterday_professors(state_id, department_type)
    if not yesterday_professors:
        LOGGER.warning('"%s": 0 professor yesterday in "%s" department', state_id, department_type)
        return
    yesterday_total = 0
    for professor in yesterday_professors:
        yesterday_total += professor.points

    institutes = get_institutes()
    uranium_institutes = []
    for institute in institutes:
        if institute['department_type'] == department_type:
            uranium_institutes.append(institute)
            if institute['state_id'] == state_id:
                state_institute = institute
    top_department = uranium_institutes[0]
    top_value = math.ceil(top_department['value'] / 10) * 10
    points_per_day = round(top_value / 14)
    msg_current = "Huidige uranium bonus is {} % met {} punten.".format(
        state_institute['current_bonus'],
        state_institute['value']
    )
    if state_institute['current_bonus'] == 10:
        msg_required = "Dagelijks zijn er {} punten nodig.".format(
            points_per_day
        )
    else:
        msg_required = "Benodigde punten voor 10 % bonus: {} wat dagelijks {} punten zijn.".format(
            top_value,
            points_per_day
        )
    msg_yesterday = "Aantal punten gisteren: {}, wat {} % van de benodigde aantal punten is.".format(
        yesterday_total,
        round(100 / points_per_day * yesterday_total)
    )
    message = ' '.join([
        msg_current,
        msg_required,
        msg_yesterday
    ])
    print(message)
    send_message(language, message)

def add_send_progress_message(state_id, department_type, language):
    """Add send_message"""
    scheduler.add_job(
        job_send_progress_message,
        'cron',
        args=[state_id, department_type, language],
        id='send_message_{}_{}'.format(state_id, department_type),
        replace_existing=True,
        hour='20',
        minute='10'
    )

if __name__ == '__main__':
    # jobs
    # job_update_department(2788, 6)
    # job_send_progress_message(2788, 6, 'nl')
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
    # uranium
    add_update_department(2604, 6)
    # De Provincien
    # gold
    add_update_department(2620, 2)

    # send message
    add_send_progress_message(2788, 6, 'nl')

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print('Exiting application')
        scheduler.shutdown()
        exit()
