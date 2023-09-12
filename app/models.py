import datetime
import pytz

from redis_om import Migrator
from redis_om import Field, JsonModel, EmbeddedJsonModel
from redis_om.model import NotFoundError
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Location'
    name: str = Field(index=True)
    abbreviation: str = Field(index=True)
    address: str = Field(index=True)
    # day_of_week: str = Field(index=True)
    # start_time: datetime.datetime
    # end_time: datetime.datetime
    deleted: int = Field(index=True, default=0)

    # def __repr__(self):
    #     # rep = self.name + ' (' + self.day_of_week + ' '+ \
    #     #     self.start_time.strftime('%I:%M%p') + ' - ' + self.end_time.strftime('%I:%M%p') + ')'
    #     return f"Location(id = {self.name})"

    # def dict(self):
    #     return {
    #         'pk': self.pk,
    #         'name': self.name,
    #         'abbreviation': self.abbreviation,
    #         'address': self.address,
    #         'day_of_week': self.day_of_week,
    #         'start_time': self.start_time.isoformat(),
    #         'end_time': self.end_time.isoformat(),
    #         'deleted': self.deleted
    #     }


class Level(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Level'
    name: str = Field(index=True)
    level: str = Field(index=True)
    abbreviation: str = Field(index=True)
    start_age: str
    end_age: str
    deleted: int = Field(index=True, default=0)

    def dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'level': self.level,
            'start_age': self.start_age,
            'end_age': self.end_age,
            'abbreviation': self.abbreviation,
            'deleted': self.deleted
        }


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
    given_name: str = Field(index=True)
    surname: str = Field(index=True)
    dob: datetime.datetime
    gender: str = Field(index=True)
    email: str = Field(index=True)
    phone: str = Field(index=True)
    wechat: str = Field(index=True)
    referer: str = Field(index=True)
    remark: str
    class_list: List[str]
    deleted: int = Field(index=True, default=0)

    def dict(self):
        return {
            'pk': self.pk,
            'given_name': self.given_name,
            'surname': self.surname,
            'dob': self.dob.isoformat(),
            'gender': self.gender,
            'email': self.email,
            'phone': self.phone,
            'wechat': self.wechat,
            'referer': self.referer,
            'remark': self.remark,
            'class_list': List[str],
            'deleted': self.deleted
        }


class Term(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Term'
    name: str = Field(index=True)
    year: str = Field(index=True)
    start_day: datetime.datetime
    end_day: datetime.datetime
    number_of_week: int = Field(index=True, default=0)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'year': self.year,
            'start_day': self.start_day.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'end_day': self.end_day.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'number_of_week': self.number_of_week,
            'deleted': self.deleted
        }


class Unchecked(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Unchecked'
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    dob: datetime.datetime
    gender: str = Field(index=True)
    wechat: str = Field(index=True)

    # location: str = Field(index=True)
    # level: str = Field(index=True)
    terms: List[str]
    class_option: str = Field(index=True)
    email: str = Field(index=True)
    phone: str = Field(index=True)
    first_emergency_contact:  str = Field(index=True)
    second_emergency_contact:  str = Field(index=True)

    find_us: str = Field(index=True)
    referer: str = Field(index=True)

    message: str
    checked: int = Field(index=True, default=0)
    verify: int = Field(index=True, default=0)
    status: str
    created: datetime.datetime
    updated: datetime.datetime
    deleted: int = Field(index=True, default=0)

    def dict(self):
        try:
           class_option = ClassOption.get(self.class_option)
        except NotFoundError:
            class_option = {"ClassOption NotFoundError"}

        # try:
        #     location = Location.get(self.level)
        # except NotFoundError:
        #     location = "Level NotFoundError"
        # try:
        #     level = Level.get(self.level)
        # except NotFoundError:
        #     level = "Level NotFoundError"
        # try:
        #     term = Term.get(self.term)
        # except NotFoundError:
        #     term = "Term NotFoundError"

        try:
            class_option = ClassOption.get(self.class_option)
        except NotFoundError:
            class_option = "ClassOption NotFoundError"
        return {
            'pk': self.pk,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.isoformat(),
            'gender': self.gender,
            'wechat': self.wechat,
            'first_emergency_contact': self.first_emergency_contact,
            'second_emergency_contact': self.second_emergency_contact,

            # 'location': location.dict(),
            # 'level': level.dict(),
            # 'term': term.dict(),
            'class_option': class_option.dict(),
            'email': self.email,
            'phone': self.phone,
            'find_us': self.find_us,
            'referer': self.referer,

            'verify': self.verify,
            'status': self.status,
            'message': self.message,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            # 'class_list': List[str],
            'deleted': self.deleted
        }


class ClassOption(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'ClassOption'
    class_code: str = Field(index=True)
    location: str = Field(index=True)
    day_of_week: str = Field(index=True)
    start_time: datetime.datetime
    end_time: datetime.datetime
    level: str = Field(index=True)
    memeo: str = Field(index=True)
    terms: List[str]
    deleted: int = Field(index=True, default=0)

    def dict(self):
        try:
            location = Location.get(self.location).dict()
        except NotFoundError:
            location = {'name': 'Location field is invaild'}

        try:
            level = Level.get(self.level).dict()
        except NotFoundError:
            level = {'name': 'Level field is invaild'}

        terms = []
        for pk in self.terms:
            try:
                term = Term.get(pk).dict()
            except NotFoundError:
                term = {}
            finally:
                terms.append(term)

        return {
            'pk': self.pk,
            'class_code': self.class_code,
            'location': location,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'end_time': self.end_time.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'terms': terms,
            'level': level,
            'memeo': self.memeo,
            'deleted': self.deleted
        }

__all__ = (
    'User',
    'Location',
    'Level',
    'Teacher',
    'Student',
)
