from importlib import import_module

from omegaconf import DictConfig

from core_lib.core_lib import CoreLib
from core_lib.web_helpers.web_helprs_utils import WebHelpersUtils

from track_core_lib.track_core_lib import TrackCoreLib


class TrackCoreLibInstance(object):
    _app_instance = None

    @staticmethod
    def init(core_lib_cfg):
        if not TrackCoreLibInstance._app_instance:
            WebHelpersUtils.init(WebHelpersUtils.ServerType.FLASK)
            TrackCoreLibInstance._app_instance = TrackCoreLib(core_lib_cfg)
        return TrackCoreLibInstance._app_instance

    @staticmethod
    def get() -> TrackCoreLib:
        return TrackCoreLibInstance._app_instance
