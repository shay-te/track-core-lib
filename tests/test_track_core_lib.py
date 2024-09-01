import unittest
from datetime import datetime

from core_lib.data_layers.data.data_helpers import build_url
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time
from pymongo import MongoClient

from tests.helpers.utils import sync_create_start_core_lib
from track_core_lib.data_layers.data.track import TrackType


def forward_time_years(years: int = 0):
    if years > 0:
        return (datetime.utcnow() + relativedelta(years=years))
    return datetime.utcnow()


class TestTrackCoreLib(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.track_core_lib = sync_create_start_core_lib()
        client = MongoClient(build_url(**cls.track_core_lib.config.core_lib.data.mongodb.url))
        # db = client['track']
        client.drop_database('track')

    def test_track(self):
        user_id = 1
        self.assertEqual(self.track_core_lib.track.count_user_document(user_id), 0)
        self.track_core_lib.track.register_entity(user_id, TrackType.FOOD, {})
        self.assertEqual(self.track_core_lib.track.count_user_document(user_id), 1)

        self.assertEqual(len(self.track_core_lib.track.all(user_id)), 1)
        self.assertEqual(len(self.track_core_lib.track.all(user_id, TrackType.FOOD)), 1)
        self.assertEqual(len(self.track_core_lib.track.all(user_id, TrackType.SLEEP)), 0)

        with freeze_time(lambda: forward_time_years(2)):
            self.track_core_lib.track.register_entity(user_id, TrackType.FOOD, {})

        self.assertEqual(len(self.track_core_lib.track.all(user_id, TrackType.FOOD)), 2)
        self.assertEqual(self.track_core_lib.track.count_user_document(user_id), 2)

        with freeze_time(lambda: forward_time_years(1)):
            self.track_core_lib.track.register_entity(user_id, TrackType.FOOD, {})

        self.assertEqual(len(self.track_core_lib.track.all(user_id, TrackType.FOOD)), 3)
        self.assertEqual(self.track_core_lib.track.count_user_document(user_id), 3)
