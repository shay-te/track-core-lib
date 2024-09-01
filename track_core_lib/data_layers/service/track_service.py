import datetime

from core_lib.cache.cache_decorator import Cache
from core_lib.data_layers.service.service import Service
from core_lib.data_transform.result_to_dict import ResultToDict
from core_lib.error_handling.status_code_exception import StatusCodeException

from track_core_lib.constants import CACHE_TRACK
from track_core_lib.data_layers.data.track import TrackType
from track_core_lib.data_layers.data_access.track_data_access import TrackDataAccess


class TrackSrvice(Service):

    CACHE_YEAR = 'user_full_{user_id}_{year}'
    CACHE_ALL = 'user_all_{user_id}_{type}'

    def __init__(self, track_data_access: TrackDataAccess):
        self._track_data_access = track_data_access

    def register_entity(self, user_id: int, type: TrackType, meta_data: dict):
        today = datetime.datetime.utcnow()
        try:
            self.get(user_id, today.year)
        except StatusCodeException:
            self._track_data_access.create(user_id, today)
        self._track_data_access.register_entity(user_id, today, type, meta_data)
        self._invalidate(user_id, today.year)
        self._invalidate_by_type(user_id, type)
        self._invalidate_by_type(user_id, None)

    @Cache(CACHE_YEAR, handler_name=CACHE_TRACK)
    @ResultToDict()
    def get(self, user_id: int, year: int):
        result = self._track_data_access.get(user_id, year)
        if result:
            result['_id'] = str(result['_id'])
        return result

    @Cache(CACHE_YEAR, handler_name=CACHE_TRACK, invalidate=True)
    def _invalidate(self, user_id: int, year: int):
        pass

    @Cache(CACHE_ALL, handler_name=CACHE_TRACK, invalidate=True)
    def _invalidate_by_type(self, user_id: int, type: TrackType):
        pass

    @Cache(CACHE_ALL, handler_name=CACHE_TRACK)
    @ResultToDict()
    def all(self, user_id: int, type: TrackType = None):
        return self._track_data_access.all(user_id, type)

    def count_user_document(self, user_id: int):
        return self._track_data_access.count_user_document(user_id)
