from typing import List, Optional
from pydantic import BaseModel, PositiveInt, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

"""Телефоны"""

class PhoneBaseSchema(BaseModel):
    number: PhoneNumber = Field(description="Номер телефона")
    organization_id: Optional[PositiveInt] = Field(description="Идентификатор организации", default=None)

    model_config = ConfigDict(from_attributes=True)

class PhoneSchema(PhoneBaseSchema):
    id: PositiveInt = Field(description="Идентификатор телефона")

class PhoneUpdateSchema(BaseModel):
    number: Optional[PhoneNumber] = Field(None, description="Номер телефона")
    organization_id: Optional[PositiveInt] = Field(None, description="Идентификатор организации")

"""Здания"""

class BuildingBaseSchema(BaseModel):
    country: str = Field(description="Страна")
    city: str = Field(description="Город")
    street: str = Field(description="Улица")
    house_number: str = Field(description="Номер дома")
    latitude: float = Field(ge=-90, le=90, description="Широта (-90..90)")
    longitude: float = Field(ge=-180, le=180, description="Долгота (-180..180)")

    model_config = ConfigDict(from_attributes=True)

class BuildingSchema(BuildingBaseSchema):
    id: PositiveInt = Field(description="Идентификатор здания")

class BuildingUpdateSchema(BaseModel):
    country: Optional[str] = Field(description="Страна", default=None)
    city: Optional[str] = Field(description="Город", default=None)
    street: Optional[str] = Field(description="Улица", default=None)
    house_number: Optional[str] = Field(description="Номер дома", default=None)
    latitude: Optional[float] = Field(ge=-90, le=90, description="Широта (-90..90)", default=None)
    longitude: Optional[float] = Field(ge=-180, le=180, description="Долгота (-180..180)", default=None)

"""Деятельности"""

class ActivitySchema(BaseModel):
    id: PositiveInt = Field(description="Идентификатор деятельности")
    name: str = Field(description="Название деятельности")

    model_config = ConfigDict(from_attributes=True)

"""Организации"""

class OrganizationBaseSchema(BaseModel):
    name: str = Field(description="Название организации")
    building_id: Optional[PositiveInt] = Field(description="Идентификатор здания", default=None)

    model_config = ConfigDict(from_attributes=True)

class OrganizationSchema(OrganizationBaseSchema):
    id: PositiveInt = Field(description="Идентификатор организации")

    phones: List[PhoneSchema] = Field(description="Телефоны организации", default_factory=list)
    building: Optional[BuildingSchema] = Field(description="Здание организации", default=None)
    activities: List[ActivitySchema] = Field(description="Виды деятельности организации", default_factory=list)

class OrganizationUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, description="Название организации")
    building_id: Optional[PositiveInt] = Field(None, description="Идентификатор здания")