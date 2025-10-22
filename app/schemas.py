from typing import List
from pydantic import BaseModel, PositiveInt, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

class PhoneSchema(BaseModel):
    id: PositiveInt = Field(description="Идентификатор телефона")
    number: PhoneNumber = Field(description="Номер телефона")
    organization_id: PositiveInt = Field(description="Идентификатор организации")

    model_config = ConfigDict(from_attributes=True)

class BuildingSchema(BaseModel):
    id: PositiveInt = Field(description="Идентификатор здания")
    country: str = Field(description="Страна")
    city: str = Field(description="Город")
    street: str = Field(description="Улица")
    house_number: str = Field(description="Номер дома")
    latitude: float = Field(ge=-90, le=90, description="Широта (-90..90)")
    longitude: float = Field(ge=-180, le=180, description="Долгота (-180..180)")

    model_config = ConfigDict(from_attributes=True)

class ActivitySchema(BaseModel):
    id: PositiveInt = Field(description="Идентификатор деятельности")
    name: str = Field(description="Название деятельности")

    model_config = ConfigDict(from_attributes=True)

class OrganizationSchema(BaseModel):
    id: PositiveInt = Field(description="Идентификатор организации")
    name: str = Field(description="Название организации")
    building_id: PositiveInt = Field(description="Идентификатор здания")

    phones: List[PhoneSchema] = Field(description="Телефоны организации")
    building: BuildingSchema = Field(description="Здание организации")
    activities: List[ActivitySchema] = Field(description="Виды деятельности организации")

    model_config = ConfigDict(from_attributes=True)