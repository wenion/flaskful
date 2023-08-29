import datetime

from redis_om import Migrator
from redis_om import Field, JsonModel, EmbeddedJsonModel
from pydantic import NonNegativeInt
from typing import Optional, List
from flask_bcrypt import generate_password_hash, check_password_hash


class User(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'User'
    # userid: str = Field(index=True)
    name: str = Field(index=True)
    email: str = Field(index=True)
    phone: str = Field(index=True)
    password: str = Field(index=True)
    deleted: int = Field(index=True, default=0)

    def hash_password(password):
        return generate_password_hash(password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Location(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Location'
    name: str = Field(index=True)
    abbreviation: str = Field(index=True)
    deleted: int = Field(index=True, default=0)


class Level(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Level'
    name: str = Field(index=True)
    level: str = Field(index=True)
    abbreviation: str = Field(index=True)
    deleted: int = Field(index=True, default=0)


class ClassItem(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'ClassItem'
    item_no: str = Field(index=True)
    item_name: str = Field(index=True)
    current_price: float = Field(index=True)
    rate: float = Field(index=True)
    gst_included: float = Field(index=True)
    comments: str = Field(index=True)
    deleted: int = Field(index=True, default=0)


class Teacher(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Teacher'
    name: str = Field(index=True)
    phone: str = Field(index=True)
    class_list: List[str]
    deleted: int = Field(index=True, default=0)


class Student(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Student'
    name: str = Field(index=True)
    phone: str = Field(index=True)
    class_list: List[str]
    deleted: int = Field(index=True, default=0)


# class ClassOption(JsonModel):
#     class Meta:
#         global_key_prefix = 's'
#         model_key_prefix = 'ClassOption'
#     name: str = Field(index=True)
#     phone: str = Field(index=True)
#     class_list: List[str]

__all__ = (
    'User',
    'Location',
    'Level',
    'Teacher',
    'Student',
)
