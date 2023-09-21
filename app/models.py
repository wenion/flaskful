import datetime
import pytz

from redis_om import Field, JsonModel, EmbeddedJsonModel
from redis_om.model import NotFoundError
from pydantic import NonNegativeInt
from typing import Optional, List
from flask_bcrypt import generate_password_hash, check_password_hash

def get_abbr_from_day(day_of_week):
    days = {
        'Monday': 'MON',
        'Tuesday': 'TUE',
        'Wednesday': 'WED',
        'Thursday': 'THU',
        'Friday': 'FRI',
        'Saturday': 'SAT',
        'Sunday': 'SUN',
        }
    return days[day_of_week]

def get_num_from_day(day_of_week):
    days = {
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7,
        }
    return days[day_of_week] 

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
    id: int = Field(index=True, sortable=True)
    name: str = Field(index=True)
    abbreviation: str = Field(index=True)
    address: str = Field(index=True)
    # day_of_week: str = Field(index=True)
    # start_time: datetime.datetime
    # end_time: datetime.datetime
    display: int = Field(index=True, default=1)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        return {
            'pk': self.pk,
            'id': self.id,
            'value': self.pk,
            'label': self.abbreviation,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'address': self.address,
            'display': self.display,
            'deleted': self.deleted
        }


class Level(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Level'
    id: int = Field(index=True, sortable=True)
    name: str = Field(index=True)
    level: str = Field(index=True)
    abbreviation: str = Field(index=True)
    start_age: str
    end_age: str
    display: int = Field(default=1)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        return {
            'pk': self.pk,
            'id': self.id,
            'value': self.pk,
            'label': self.abbreviation,
            'name': self.name,
            'level': self.level,
            'start_age': self.start_age,
            'end_age': self.end_age,
            'abbreviation': self.abbreviation,
            'display': self.display,
            'deleted': self.deleted
        }


class ClassItem(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'ClassItem'
    id: int = Field(sortable=True)
    item_no: str = Field(index=True)
    item_name: str = Field(index=True)
    current_price: float = Field(index=True)
    rate: float = Field(index=True, default=1.1)
    gst_included: float = Field(index=True)
    comments: str = Field(index=True)
    display: int = Field(index=True, default=1)
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
    id: int = Field(sortable=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    dob: datetime.datetime
    gender: str = Field(index=True)
    wechat: str = Field(index=True)
    email: str = Field(index=True)
    phone: str = Field(index=True)
    first_emergency_contact:  str = Field(index=True)
    second_emergency_contact:  str = Field(index=True)

    referer: str = Field(index=True)
    # remark: str
    # class_list: List[str]
    created: datetime.datetime
    updated: datetime.datetime
    display: int = Field(default=1)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        return {
            'pk': self.pk,
            'id': self.id,
            'value': self.pk,
            'label': self.first_name + ' ' + self.last_name + ' ('+ self.phone + ')',
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.isoformat(),
            'gender': self.gender,
            'wechat': self.wechat,
            'email': self.email,
            'phone': self.phone,

            'first_emergency_contact': self.first_emergency_contact,
            'second_emergency_contact': self.second_emergency_contact,
            'referer': self.referer,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            'display': self.display,
            'deleted': self.deleted
        }


class Term(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Term'
    id: int = Field(sortable=True)
    name: str = Field(index=True)
    year: str = Field(index=True)
    start_day: datetime.datetime
    end_day: datetime.datetime
    number_of_week: int = Field(index=True, default=0)
    display: int = Field(index=True, default=1)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        return {
            'pk': self.pk,
            'id': self.id,
            'value': self.pk,
            'label': self.name + ' ('+ self.year +')',
            'name': self.name,
            'year': self.year,
            'start_day': self.start_day.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'end_day': self.end_day.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'number_of_week': self.number_of_week,
            'display': self.display,
            'deleted': self.deleted
        }


class Unchecked(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Unchecked'
    id: int = Field(sortable=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    dob: datetime.datetime
    gender: str = Field(index=True)
    wechat: str = Field(index=True)

    term: str = Field(index=True)
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
    display: int = Field(default=1)
    student: str = Field(index=True)
    plan_lesson: str = Field(index=True)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        try:
           class_option = ClassOption.get(self.class_option).dict()
        except NotFoundError:
            class_option = {
                'label': 'ClassOption field is invaild',
                'value': 'invaild'
                }
            
            location = {
                'label': 'Location field is invaild',
                'value': 'invaild'
                }
            
            level = {
                'label': 'Level field is invaild',
                'value': 'invaild'
                }
        else:
            location = class_option['location']
            level = class_option['level']

        print("clas option", class_option)

        # student
        # plan_lesson

        return {
            'pk': self.pk,
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dob': self.dob.isoformat(),
            'gender': self.gender,
            'wechat': self.wechat,
            'first_emergency_contact': self.first_emergency_contact,
            'second_emergency_contact': self.second_emergency_contact,

            'location': location,
            'level': level,
            'term': self.term,
            'class_option': class_option,
            'email': self.email,
            'phone': self.phone,
            'find_us': self.find_us,
            'referer': self.referer,

            'verify': self.verify,
            'status': self.status,
            'message': self.message,
            'created': self.created.isoformat(),
            'updated': self.updated.isoformat(),
            'student': "test",
            'plan_lesson': "test",
            # 'class_list': List[str],
            'deleted': self.deleted
        }


class ClassOption(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'ClassOption'
    id: int = Field(index=True, sortable=True)
    class_code: str = Field(index=True)
    location: str = Field(index=True)
    day_of_week: str = Field(index=True)
    start_time: datetime.datetime
    end_time: datetime.datetime
    level: str = Field(index=True)
    memeo: str = Field(index=True)
    year: str = Field(index=True)
    display: int = Field(index=True, default=1)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        try:
            location = Location.get(self.location).dict()
        except NotFoundError:
            location = {
                'label': 'Location field is invaild',
                'value': 'invaild'
                }

        try:
            level = Level.get(self.level).dict()
        except NotFoundError:
            level = {
                'label': 'Level field is invaild',
                'value': 'invaild'
                }

        return {
            'pk': self.pk,
            'id': self.id,
            'value': self.pk,
            'label': self.class_code + ' ('+ self.year + ')',
            'class_code': self.class_code,
            'location': location,
            'day_of_week': {
                'value': self.day_of_week,
                'label': get_abbr_from_day(self.day_of_week)
            },
            'start_time': self.start_time.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'end_time': self.end_time.astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'year': self.year,
            'display': self.display,
            'level': level,
            'memeo': self.memeo,
            'deleted': self.deleted
        }


class Lesson(JsonModel):
    class Meta:
        global_key_prefix = 's'
        model_key_prefix = 'Lesson'
    id: int = Field(sortable=True)
    class_option_pk: str = Field(index=True)
    term_pk: str = Field(index=True)
    class_code: str = Field(index=True)
    # level: str = Field(index=True)
    # location: str = Field(index=True)
    date: datetime.datetime
    # start_time: datetime.datetime
    # end_time: datetime.datetime
    # term: str = Field(index=True)
    year: str = Field(index=True)
    week: int = Field(index=True)
    students: List[str]
    teacher: str# = Field(index=True)
    deleted: int = Field(index=True, default=0)

    def dict(self):
        try:
            class_option = ClassOption.get(self.class_option_pk).dict()
        except NotFoundError:
            class_option = {
                'label': 'Class Option field is invaild',
                'value': 'invaild'
                }

        try:
            term = Term.get(self.term_pk).dict()
        except NotFoundError:
            term = {
                'label': 'Term field is invaild',
                'value': 'invaild'
                }
        return {
            'pk': self.pk,
            'id': self.id,
            'value': self.pk,
            # 'label': self.class_code + ' (' + class_option['start_time'].astimezone(pytz.timezone("Australia/Sydney")).isoformat() + \
            #     '' + class_option['end_time'].astimezone(pytz.timezone("Australia/Sydney")).isoformat() + ')',
            'class_code': self.class_code,
            'class_option_pk': self.class_option_pk,
            'term_pk': self.term_pk,
            'level': class_option['level'],
            'location': class_option['location'],
            'day_of_week': class_option['day_of_week'],
            'date': self.date.isoformat(),
            # 'start_day': term['start_day'].astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            # 'end_day': term['end_day'].astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            # 'start_time': class_option['start_time'].astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            # 'end_time': class_option['end_time'].astimezone(pytz.timezone("Australia/Sydney")).isoformat(),
            'class_option': class_option,
            'term': term,
            'year': self.year,
            'week': self.week,
            'students': self.students,
            'teacher': self.teacher,
            'deleted': self.deleted
        }


__all__ = (
    'User',
    'Location',
    'Level',
    'Teacher',
    'Student',
)
