from sqlmodel import SQLModel, Field, Relationship
from typing import Annotated
from pydantic import field_validator, BaseModel
from pydantic import Field as PydanticField


HYDROPONIC_MAX_TEMPERATURE: float = 25.0
HYDROPONIC_MIN_TEMPERATURE: float = 5.0
HYDROPONIC_MIN_PH:          float = 0.0
HYDROPONIC_MAX_PH:          float = 14.0


class Hydroponic(SQLModel, table=True):
    __table_args__ = {"implicit_returning": False} # due to https://docs.sqlalchemy.org/en/20/dialects/mssql.html#triggers

    id:                     Annotated[int | None, Field(default=None, primary_key=True)] = None
    user_id_owner:          Annotated[int | None, Field(default=None, foreign_key="user.id", nullable=False, ondelete="CASCADE")] = None
    name:                   Annotated[str, Field(nullable=False, min_length=1, max_length=255)]

    water_amount:           Annotated[float, Field(gt=0, nullable=False)]
    water_consumption:      Annotated[float, Field(gt=0, nullable=False)]

    minerals_amount:        Annotated[float, Field(gt=0, nullable=False)]
    minerals_optimal:       Annotated[float, Field(gt=0, nullable=False)]
    minerals_consumption:   Annotated[float, Field(gt=0, nullable=False)]

    acidity_optimal_ph:     Annotated[float, Field(ge=HYDROPONIC_MIN_PH, le=HYDROPONIC_MAX_PH, nullable=False)]
    temperature_C_optimal:  Annotated[float, Field(ge=HYDROPONIC_MIN_TEMPERATURE, le=HYDROPONIC_MAX_TEMPERATURE, nullable=False)]

    oxygen_amount:          Annotated[float, Field(gt=0, nullable=False)]
    oxygen_consumption:     Annotated[float, Field(gt=0, nullable=False)]

    value_water:            Annotated[float, Field(ge=0, nullable=False)]
    value_minerals:         Annotated[float, Field(ge=0, nullable=False)]
    value_acidity_ph:       Annotated[float, Field(ge=HYDROPONIC_MIN_PH, le=HYDROPONIC_MAX_PH, nullable=False)]
    value_temperature_C:    Annotated[float, Field(ge=HYDROPONIC_MIN_TEMPERATURE, le=HYDROPONIC_MAX_TEMPERATURE, nullable=False)]
    value_oxygen:           Annotated[float, Field(ge=0, nullable=False)]

    # --- validators ---

    @field_validator("value_water", mode='after')
    @classmethod
    def check_value_water(cls, value: float, info) -> float:
        water_amount = info.data["water_amount"]
        if value > water_amount:
            raise ValueError("value_water exceeds the allowed (declared by water_amount) limits")
        return value

    @field_validator("value_minerals", mode='after')
    @classmethod
    def check_value_minerals(cls, value: float, info) -> float:
        minerals_amount = info.data["minerals_amount"]
        if minerals_amount is not None and value > minerals_amount:
            raise ValueError("value_minerals exceeds the allowed (declared by minerals_amount) limits")
        return value

    @field_validator("value_oxygen", mode='after')
    @classmethod
    def check_value_oxygen(cls, value: float, info) -> float:
        oxygen_amount = info.data["oxygen_amount"]
        if oxygen_amount is not None and value > oxygen_amount:
            raise ValueError("value_oxygen exceeds the allowed (declared by oxygen_amount) limits")
        return value


class User(SQLModel, table=True):
    id:              Annotated[int | None, Field(default=None, primary_key=True, nullable=False)] = None # default = None - cause it is set by DB
    username:        Annotated[str, Field(unique=True, nullable=False)]
    hash_salt:       Annotated[str, Field()]

    hydroponics: list[Hydroponic] = Relationship(back_populates=None, passive_deletes=True)


# ------------------------------------------------------------------------------------------------------------
# Response Models
# ------------------------------------------------------------------------------------------------------------

class Hydroponic_response(BaseModel):
    id: int | None
    name: str
    water_amount: float
    water_consumption: float
    minerals_amount: float
    minerals_optimal: float
    minerals_consumption: float
    acidity_optimal_ph: float
    temperature_C_optimal: float
    oxygen_amount: float
    oxygen_consumption: float
    value_water: float
    value_minerals: float
    value_acidity_ph: float
    value_temperature_C: float
    value_oxygen: float

    class Config:
        from_attributes = True


class Hydroponic_input(BaseModel):
    name:                   Annotated[str, PydanticField(min_length=1, max_length=255)]

    water_amount:           Annotated[float, PydanticField(gt=0)]
    water_consumption:      Annotated[float, PydanticField(gt=0)]

    minerals_amount:        Annotated[float, PydanticField(gt=0)]
    minerals_optimal:       Annotated[float, PydanticField(gt=0)]
    minerals_consumption:   Annotated[float, PydanticField(gt=0)]

    acidity_optimal_ph:     Annotated[float, PydanticField(ge=HYDROPONIC_MIN_PH,          le=HYDROPONIC_MAX_PH)]
    temperature_C_optimal:  Annotated[float, PydanticField(ge=HYDROPONIC_MIN_TEMPERATURE, le=HYDROPONIC_MAX_TEMPERATURE)]

    oxygen_amount:          Annotated[float, PydanticField(gt=0)]
    oxygen_consumption:     Annotated[float, PydanticField(gt=0)]