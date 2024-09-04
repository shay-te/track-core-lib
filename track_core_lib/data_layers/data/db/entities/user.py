import enum

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import SoftDeleteMixin
from core_lib.helpers.validation import is_email
from sqlalchemy import Column, Integer, VARCHAR, LargeBinary, Index
from sqlalchemy.orm import validates
from core_lib.data_layers.data.db.sqlalchemy.types.int_enum import IntEnum


class User(Base, SoftDeleteMixin):

    __tablename__ = 'user'

    INDEX_EMAIL = 'index_email'

    class Gender(enum.Enum):
        MALE = 1
        FEMALE = 2

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(VARCHAR(length=255), nullable=False)
    password = Column(LargeBinary(length=255))
    first_name = Column(VARCHAR(length=255))
    middle_name = Column(VARCHAR(length=255))
    last_name = Column(VARCHAR(length=255))
    gender = Column('gender', IntEnum(Gender))

    @validates('email')
    def validate_email(self, key, email):
        if not email or not is_email(email):
            raise AssertionError(f'email is invalid. {email}')
        return email

    __table_args__ = (Index(INDEX_EMAIL, 'email', unique=True),)
