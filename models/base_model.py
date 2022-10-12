#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
                    Column, ForeignKey, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if len(kwargs) != 0:
                if "id" not in kwargs.keys():
                    self.id = str(uuid.uuid4())
                if "created_at" not in kwargs.keys():
                    self.created_at = datetime.now()
                if "updated_at" not in kwargs.keys():
                    self.updated_at = datetime.now()
                for key, value in kwargs.items():
                    if key == "__class__":
                        continue
                    if key == "created_at" or key == "updated_at":
                        kwargs[key] = datetime. \
                                      strptime(kwargs[key],
                                               '%Y-%m-%dT%H:%M:%S.%f')
                        setattr(self, key, kwargs[key])
                    else:
                        setattr(self, key, value)
            try:
                del kwargs['__class__']
            except Exception as exception:
                self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        # if dictionary.has_key('_sa_instance_state'):
        if '_sa_instance_state' in dictionary:
            dictionary.pop('_sa_instance_state')
        return dictionary

    def delete(self):
        objects = storage.all()
        copy_objects = {}
        copy_objects.update(objects)
        for key, val in copy_objects.items():
            if val is self:
                objects.pop(key)
        objects.save()
