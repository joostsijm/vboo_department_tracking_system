"""Database module"""

from app import Session
from app.models import Player, State, Department, DepartmentStat


def get_latest_professor(state_id, department_type):
    """Get latest professor from database"""
    return None

def save_professors(state_id, department_type, professors):
    """Save professors to database"""
    session = Session()
    resource_track.state_id = state_id
    resource_track.resource_id = resource_id
    session.add(resource_track)
    session.commit()

    for region_id, region in regions.items():
        resource_stat = ResourceStat()
        resource_stat.region_id = region_id
        resource_stat.explored = region['explored']
        resource_stat.deep_exploration = region['deep_exploration']
        resource_stat.limit_left = region['limit_left']
        session.add(resource_stat)
    session.commit()
