from core_lib.connection.sql_alchemy_connection_registry import SqlAlchemyConnectionRegistry
from omegaconf import DictConfig
import os
import inspect
from core_lib.alembic.alembic import Alembic
from core_lib.core_lib import CoreLib
from core_lib.cache.cache_handler_ram import CacheHandlerRam

from track_core_lib.constants import CACHE_TRACK
from track_core_lib.data_layers.data.db.entities.exercise import Exercise
from track_core_lib.data_layers.data.db.entities.user import User
from track_core_lib.data_layers.data_access.exercise_data_access import ExerciseDataAccess
from track_core_lib.data_layers.service.exercise_service import ExerciseService


class TrackCoreLib(CoreLib):
    def __init__(self, conf: DictConfig):
        super().__init__()
        self.config = conf
        CoreLib.cache_registry.register(CACHE_TRACK, CacheHandlerRam())
        User
        Exercise
        db_connection_reg = SqlAlchemyConnectionRegistry(self.config.core_lib.data.sqlalchemy)
        self.exercise = ExerciseService(ExerciseDataAccess(db_connection_reg))

    @staticmethod
    def install(cfg: DictConfig):
        Alembic(os.path.dirname(inspect.getfile(TrackCoreLib)), cfg).upgrade()

    @staticmethod
    def uninstall(cfg: DictConfig):
        Alembic(os.path.dirname(inspect.getfile(TrackCoreLib)), cfg).downgrade()
