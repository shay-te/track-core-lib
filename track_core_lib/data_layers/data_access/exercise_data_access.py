import datetime
import logging

from core_lib.connection.sql_alchemy_connection_registry import SqlAlchemyConnectionRegistry
from core_lib.data_layers.data_access.data_access import DataAccess
from core_lib.error_handling.not_found_decorator import NotFoundErrorHandler
from core_lib.helpers.validation import is_int_enum
from core_lib.rule_validator.rule_validator import ValueRuleValidator, RuleValidator
from core_lib.rule_validator.rule_validator_decorator import ParameterRuleValidator

from track_core_lib.data_layers.data.db.entities.exercise import Exercise

allowed_update_types = [
    ValueRuleValidator(Exercise.user_id.key, int),
    ValueRuleValidator(Exercise.duration_minutes.key, int),
    ValueRuleValidator(Exercise.start_datetime.key, datetime.datetime),
    ValueRuleValidator(Exercise.type.key, int, custom_converter=lambda value: Exercise.ExerciseType(value), custom_validator=lambda value: is_int_enum(value, Exercise.ExerciseType)),
]
rule_validator = RuleValidator(allowed_update_types)


class ExerciseDataAccess(DataAccess):

    def __init__(self, db: SqlAlchemyConnectionRegistry):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._db = db

    def create(self, user_id: int, type: Exercise.ExerciseType, duration_minutes: int, start_datetime: datetime.datetime):
        with self._db.get() as session:
            exercise = Exercise()
            exercise.user_id = user_id
            exercise.type = type
            exercise.duration_minutes = duration_minutes
            exercise.start_datetime = start_datetime
            session.add(exercise)
        return exercise

    @NotFoundErrorHandler()
    def get(self, exercise_id: int):
        with self._db.get() as session:
            return session.query(Exercise).filter(Exercise.id == exercise_id, Exercise.deleted_at == None).first()

    @ParameterRuleValidator(rule_validator, 'data')
    def update(self, exercise_id: int, data: dict):
        with self._db.get() as session:
            return session.query(Exercise).filter(Exercise.id == exercise_id, Exercise.deleted_at == None) \
                            .update(data)

    def all(self, user_id: int):
        with self._db.get() as session:
            return session.query(Exercise).filter(Exercise.user_id == user_id, Exercise.deleted_at == None).all()
