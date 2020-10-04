from sqlalchemy import Column, String, Integer

from ..setup_db import db


class Category(db.Model):
    '''Category'''
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    @property
    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
