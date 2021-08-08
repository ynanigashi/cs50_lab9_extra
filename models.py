from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

"""
Tables
"""
class Birthdays(Base):
    __tablename__ = 'birthdays'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    month = Column(Integer)
    day = Column(Integer)

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}, birthday: {self.month} / {self.day}'