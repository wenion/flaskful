import datetime

from redis_om import Migrator
from redis_om import Field, JsonModel, EmbeddedJsonModel
from pydantic import NonNegativeInt
from typing import Optional
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

__all__ = (
    'User',
    'Location',
    'Level',
)
