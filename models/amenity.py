#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import Base
from models.base_model import BaseModel
from os import getenv
import sqlalchemy
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    Represents Amenity for MySQL database
    Inherits from SQLAlchemy Base and connects to MySQL table amenities.

    Attributes:
        __tablename__ (str): Name of MySQL table storing amenities
        name (sqlalchemy String): Amenity name
        place_amenities (sqlalchemy relationship): Place-Amenity relationship
    """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
