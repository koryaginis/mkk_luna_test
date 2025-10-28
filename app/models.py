from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table

Base = declarative_base()

organizations_activities = Table(
    'organizations_activities',
    Base.metadata,
    Column("organization_id", Integer, ForeignKey("organizations.id"), primary_key=True),
    Column("activity_id", Integer, ForeignKey("activities.id"), primary_key=True)
)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # Название организации
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=True) # Идентификатор здания организации

    phones = relationship("Phone", back_populates="organization", cascade="all, delete-orphan")
    building = relationship("Building", back_populates="organizations")
    activities = relationship('Activity', secondary=organizations_activities, back_populates="organizations")

class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, nullable=False) # Номер телефона
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True) # Идентификатор организации

    organization = relationship("Organization", back_populates="phones")

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    country = Column(String, nullable=True) # Страна
    city = Column(String, nullable=False) # Город
    street = Column(String, nullable=False) # Улица
    house_number = Column(String, nullable=False) # Номер дома
    latitude = Column(Float, nullable=True) # Широта
    longitude = Column(Float, nullable=True) # Долгота

    organizations = relationship("Organization", back_populates="building")

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # Название вида деятельности
    path = Column(String, nullable=False) # Ссылка на деятельность в древовидной структуре

    organizations = relationship('Organization', secondary=organizations_activities, back_populates="activities")
