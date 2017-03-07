from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time
from sqlalchemy.orm import relationship
from base import Base
from time import time

class Vocabulary_Table(Base):
    """"""
    __tablename__ = "vocabulary_table"
    __table_args__ = {'extend_existing': True}

    card_id = Column(Integer, primary_key=True)
    front = Column(String)
    back = Column(String)
    date_next_practice = Column(Date,  nullable=True)
    deck = Column(Integer)
    createdDate = Column(Date)
    course_name = Column(String)
    lesson_name = Column(String)
    activities = relationship('Activity_Table', backref='card', lazy='dynamic')

    # ----------------------------------------------------------------------
    def __init__(self,  front, back, date_next_practice, deck, createdDate, course_name, lesson_name):
        """"""
        self.front = front
        self.back = back
        self.date_next_practice = date_next_practice
        self.deck = deck
        self.createdDate = createdDate
        self.course_name = course_name
        self.lesson_name = lesson_name

class Deleted_Vocabulary_Table(Base):
    """"""
    __tablename__ = "deleted_vocabulary_table"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    delete_date = Column(String)
    front = Column(String)
    back = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, front, back, delete_date):
        """"""
        self.delete_date = delete_date
        self.front = front
        self.back = back


class Config_Table(Base):
    """"""
    __tablename__ = "config_table"
    __table_args__ = {'extend_existing': True}

    key = Column(String, primary_key=True)
    value = Column(String)
    changedDate = Column(Integer)

    # ----------------------------------------------------------------------
    def __init__(self, key, value):
        """"""
        self.key = key
        self.value = value
        self.changedDate = int(time())

# SINGLE TABLE WHICH INCLUDES THE DATABASE VERSION
class Metadata_Table(Base):
    """"""
    __tablename__ = "metadata_table"
    __table_args__ = {'extend_existing': True}

    key = Column(String, primary_key=True)
    value = Column(String)



    # ----------------------------------------------------------------------
    def __init__(self, key, value):
        """"""
        self.key = key
        self.value = value

# SINGLE TABLE WHICH INCLUDES THE DATABASE VERSION
class Activity_Table(Base):
    """"""
    __tablename__ = "activity_table"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, ForeignKey('vocabulary_table.card_id'))
    date = Column(Date)
    value = Column(String) # Could be: "right", "wrong", "word_completed",

    # ----------------------------------------------------------------------
    def __init__(self, value, card_id):
        """"""
        self.timestamp = time()
        self.value = value
        self.card_id = card_id


