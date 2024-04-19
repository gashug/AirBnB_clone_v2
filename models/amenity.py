#!/usr/bin/python
""" Module that holds class Amenity """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """ Representation of Amenity """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    if models.storage_t == 'db':
        place_amenities = relationship(
            "Place", secondary="place_amenity", back_populates="amenities")
