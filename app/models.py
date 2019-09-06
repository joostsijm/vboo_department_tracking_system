"""Database models"""

from sqlalchemy import Column, ForeignKey, Integer, String, \
    SmallInteger, DateTime, BigInteger, Date
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Player(Base):
    """Model for player"""
    __tablename__ = 'player'
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    nation = Column(String)
    registration_date = Column(Date)


class State(Base):
    """Model for state"""
    __tablename__ = 'state'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Department(Base):
    """Model for department"""
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_type = Column(Integer)

    state_id = Column(Integer, ForeignKey('state.id'))
    state = relationship(
        'State',
        backref=backref('elections', lazy='dynamic')
    )


class DepartmentStat(Base):
    """Model for departent stat"""
    __tablename__ = 'department_stat'
    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime)
    points = Column(SmallInteger)

    player_id = Column(BigInteger, ForeignKey('player.id'))
    player = relationship(
        'Player',
        backref=backref('department_stats', lazy='dynamic')
    )

    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        'Department',
        backref=backref('department_stats', lazy='dynamic')
    )
