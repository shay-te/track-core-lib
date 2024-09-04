import datetime

from core_lib.cache.cache_decorator import Cache
from core_lib.data_layers.service.service import Service
from core_lib.data_transform.result_to_dict import ResultToDict

from track_core_lib.constants import CACHE_TRACK
from track_core_lib.data_layers.data.db.entities.exercise import Exercise
from track_core_lib.data_layers.data_access.exercise_data_access import ExerciseDataAccess


class ExerciseService(Service):

    CACHE_EXERCISE = 'exercise_{exercise_id}'

    def __init__(self, exercise_data_access: ExerciseDataAccess):
        self._exercise_data_access = exercise_data_access

    @ResultToDict()
    def create(self, user_id: int, type: Exercise.ExerciseType, duration_minutes: int, start_datetime: datetime.datetime):
        return self._exercise_data_access.create(user_id, type, duration_minutes, start_datetime)

    @Cache(CACHE_EXERCISE, handler_name=CACHE_TRACK)
    @ResultToDict()
    def get(self, exercise_id: int):
        return self._exercise_data_access.get(exercise_id)

    @Cache(CACHE_EXERCISE, handler_name=CACHE_TRACK, invalidate=True)
    @ResultToDict()
    def update(self, exercise_id: int, data: dict):
        return self._exercise_data_access.update(exercise_id, data)

    @ResultToDict()
    def all(self, user_id: int):
        return self._exercise_data_access.all(user_id)
