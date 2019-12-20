"""General functions module"""

import math

from app import LOGGER, database, api


def update_department(state_id, department_type):
    """Update department professors"""
    LOGGER.info('"%s": Run update for "%s" department for state', state_id, department_type)
    latest_professor = database.get_latest_professor(state_id, department_type)
    date = None
    if latest_professor:
        date = latest_professor.date_time
    professors = api.get_professors(state_id, department_type, date)
    LOGGER.info(
        '"%s": Found "%s" new professors in "%s" department',
        state_id, len(professors), department_type
    )
    # print_professors(professors)
    database.save_professors(state_id, department_type, professors)
    LOGGER.info('"%s": saved professors', state_id)


def send_progress_message(state_id, department_type, language):
    """Update department professors"""
    LOGGER.info('"%s": Send progress message for "%s" department', state_id, department_type)
    yesterday_professors = database.get_yesterday_professors(state_id, department_type)
    if not yesterday_professors:
        LOGGER.warning('"%s": 0 professor yesterday in "%s" department', state_id, department_type)
        return
    yesterday_total = 0
    for professor in yesterday_professors:
        yesterday_total += professor.points

    institutes = api.get_institutes()
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
        msg_required = \
            "Benodigde punten voor 10 % bonus: {} wat dagelijks {} punten zijn.".format(
                top_value,
                points_per_day
            )
    msg_yesterday = \
        "Aantal punten gisteren: {}, wat {} % van de benodigde aantal punten is.".format(
            yesterday_total,
            round(100 / points_per_day * yesterday_total)
        )
    message = ' '.join([
        msg_current,
        msg_required,
        msg_yesterday
    ])
    print(message)
    api.send_message(language, message)
