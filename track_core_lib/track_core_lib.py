from core_lib.connection.mongodb_connection_registry import MongoDBConnectionRegistry
from omegaconf import DictConfig
import os
import inspect
from core_lib.alembic.alembic import Alembic
from core_lib.core_lib import CoreLib
from core_lib.cache.cache_handler_memcached import CacheHandlerMemcached
from core_lib.data_layers.data.data_helpers import build_url
from core_lib.cache.cache_handler_ram import CacheHandlerRam

from track_core_lib.constants import CACHE_TRACK
from track_core_lib.data_layers.data_access.track_data_access import TrackDataAccess
from track_core_lib.data_layers.service.track_service import TrackSrvice


class TrackCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf
        mongodb = MongoDBConnectionRegistry(self.config.core_lib.data.mongodb)
        CoreLib.cache_registry.register(CACHE_TRACK, CacheHandlerRam())
        self.track = TrackSrvice(TrackDataAccess(mongodb))


    @staticmethod
    def install(cfg: DictConfig):
        Alembic(os.path.dirname(inspect.getfile(TrackCoreLib)), cfg).upgrade()

    @staticmethod
    def uninstall(cfg: DictConfig):
        Alembic(os.path.dirname(inspect.getfile(TrackCoreLib)), cfg).downgrade()
