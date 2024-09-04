import enum

from core_lib.data_layers.data.db.sqlalchemy.mixins.soft_delete_mixin import SoftDeleteMixin
from sqlalchemy import Column, Integer, Index, DateTime, ForeignKey

from core_lib.data_layers.data.db.sqlalchemy.base import Base
from core_lib.data_layers.data.db.sqlalchemy.types.int_enum import IntEnum


class Exercise(Base, SoftDeleteMixin):

    __tablename__ = 'exercise'

    INDEX_TYPE = 'index_type'

    class ExerciseType(enum.Enum):
        WALK = 1
        RUN = 2
        BICYCLE = 3
        YOGA_PILATES = 4
        FOOTBALL = 5
        BASKET_BALL = 6
        SWIMMING = 7
        AEROBIC = 8
        MEDITATION = 9
        OTHER = 100

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False) # ForeignKey("user.id")
    type = Column('type', IntEnum(ExerciseType), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    start_datetime = Column(DateTime, nullable=False)

    __table_args__ = (Index(INDEX_TYPE, 'type', unique=False),)
