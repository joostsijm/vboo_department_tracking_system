"""Database module"""

from datetime import datetime, timedelta

from app import SESSION
from app.models import Player, Department, DepartmentStat


def get_latest_professor(state_id, department_type):
    """Get latest professor from database"""
    session = SESSION()
    department = get_department(session, state_id, department_type)
    professor = department.department_stats.order_by(DepartmentStat.date_time.desc()).first()
    session.close()
    return professor

def get_player(session, player_id, player_name):
    """Get player from database"""
    player = session.query(Player).get(player_id)
    if player is None:
        player = Player()
        player.id = player_id
        player.name = player_name
        session.add(player)
        session.commit()
    return player

def get_department(session, state_id, department_type):
    """Get department from database"""
    department = session.query(Department).filter(
        Department.state_id == state_id
    ).filter(
        Department.department_type == department_type
    ).first()
    if department is None:
        department = Department()
        department.state_id = state_id
        department.department_type = department_type
        session.add(department)
        session.commit()
    return department

def save_professors(state_id, department_type, professors):
    """Save professors to database"""
    session = SESSION()
    department = get_department(session, state_id, department_type)

    for professor in professors:
        player = get_player(session, professor['id'], professor['name'])
        department_stat = DepartmentStat()
        department_stat.department_id = department.id
        department_stat.date_time = professor['date_time']
        department_stat.points = professor['points']
        department_stat.player_id = player.id
        session.add(department_stat)
    session.commit()
    session.close()

def get_yesterday_professors(state_id, department_type):
    """Get professors from yesterday"""
    session = SESSION()
    department = get_department(session, state_id, department_type)
    until_date = datetime.today().replace(hour=20, minute=0, second=0)
    from_date = until_date - timedelta(1)
    professors = session.query(DepartmentStat) \
        .filter(DepartmentStat.department_id == department.id) \
        .filter(DepartmentStat.date_time >= from_date) \
        .filter(DepartmentStat.date_time < until_date) \
        .all()
    return professors
