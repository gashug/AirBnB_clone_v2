#!/usr/bin/python3
""" Module that holds class Place """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


if models.storage_t == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey('places.id'), primary_key=True),
                          Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True))


class Place(BaseModel, Base):
    """ Representation of Place """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    reviews = relationship("Review", backref="place")
    amenities = relationship(
        "Amenity", secondary="place_amenity", back_populates="place_amenities")

    if models.storage_t != 'db':
        @property
        def reviews(self):
            """ Getter attribute to return the list of Review instances """
            from models.review import Review
            review_list = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """ Getter attribute to return the list of Amenity instances """
            amenity_list = []
            for amenity in self.amenity_ids:
                amenity_instance = models.storage.get("Amenity", amenity)
                if amenity_instance:
                    amenity_list.append(amenity_instance)
            return amenity_list

        @amenities.setter
        def amenities(self, amenity_obj):
            """ Setter attribute to handle appending Amenity.id to amenity_ids """
            if isinstance(amenity_obj, models.Amenity):
                self.amenity_ids.append(amenity_obj.id)
                self.save()
