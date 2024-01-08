#!/usr/bin/python3
"""Defines BaseModel class."""
import models
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from os import getenv
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """
    Defines BaseModel Class

    Attributes:
        id (sqlalchemy String): BaseModel id
        created_at (sqlalchemy DateTime): datetime at creation.
        updated_at (sqlalchemy DateTime): datetime of last update
    """
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
        Initializes new BaseModel

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        for key, value in kwargs.items():
            if key == '__class__':
                continue
            setattr(self, key, value)
            if type(self.created_at) is str:
                self.created_at = datetime.strptime(self.created_at, time)
            if type(self.updated_at) is str:
                self.updated_at = datetime.strptime(self.updated_at, time)

    def __str__(self):
        """string representation of BaseModel"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Return dictionary representation of BaseModel Instance
        Includes the value/key pair __class__
        which represents the class name of object
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """Delete current instance from storage"""
        models.storage.delete(self)
