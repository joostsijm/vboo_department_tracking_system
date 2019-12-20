"""API module"""

import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from app import BASE_URL, HEADERS

def get_professors(state_id, department_type, start_date):
    """Download list of professors"""
    professors = []
    not_reached_date = True
    page = 0
    while not_reached_date:
        tmp_professors = download_department(state_id, department_type, page)
        if not tmp_professors:
            not_reached_date = False
            break
        # tmp_professors = read_department()
        for professor in tmp_professors:
            if start_date is not None and professor['date_time'] <= start_date:
                not_reached_date = False
                break
            professors.append(professor)

        page += 1

    professors.reverse()
    return professors

def download_department(state_id, department_type, page):
    """Download the department"""
    response = requests.get(
        '{}listed/professors/{}/{}/{}'.format(BASE_URL, department_type, state_id, page*25),
        headers=HEADERS
    )
    return parse_department(response.text)

def read_department():
    """Read from department file"""
    with open('department.html') as file:
        return parse_department(file)

def parse_department(html):
    """Parse html return professors"""
    soup = BeautifulSoup(html, 'html.parser')
    professors_tree = soup.find_all(class_='list_link')
    professors = []
    today = datetime.strftime(datetime.now(), '%-d %B %Y')
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%-d %B %Y')
    for professor_tree in professors_tree:
        columns = professor_tree.find_all('td')
        date = columns[3].string
        date = date.replace('Today ', today)
        date = date.replace('Yesterday ', yesterday)
        professors.append({
            'id': int(re.sub(r'^.*\/', '', columns[1]['action'])),
            'name': re.sub(r'\s\(.*$', '', columns[1].string),
            'points': int(re.sub(r'^.*\(\+|\)$', '', columns[1].string)),
            'date_time': datetime.strptime(date, '%d %B %Y %H:%M'),
        })
    return professors

def get_institutes():
    """Get all institutes"""
    # return read_institutes()
    return download_institutes()

def download_institutes():
    """Download the department"""
    response = requests.get(
        '{}listed/institutes'.format(BASE_URL),
        headers=HEADERS
    )
    return parse_institutes(response.text)

def read_institutes():
    """Read from department file"""
    with open('institutes.html') as file:
        return parse_institutes(file)

def parse_institutes(html):
    """Parse html to institute list"""
    soup = BeautifulSoup(html, 'html.parser')
    institutes_tree = soup.find_all(class_='list_link')
    institutes = []
    for institute_tree in institutes_tree:
        department_type = \
            int(re.sub(r'^.*\/', '', institute_tree.select('.results_date')[1]['action']))
        value = int(institute_tree.select('.list_level')[0].string)
        current_bonus = float(re.sub(r'\s%$', '', institute_tree.select('.list_level')[2].string))
        if current_bonus >= 2:
            institutes.append({
                'state_id': int(institute_tree['user']),
                'department_type': department_type,
                'current_bonus': current_bonus,
                'value': value,
            })
    return institutes

def send_message(language, message):
    """Send chat message"""
    requests.post(
        '{}send_chat/{}'.format(BASE_URL, language),
        headers=HEADERS,
        data={'message': message}
    )
