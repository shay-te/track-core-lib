import unittest
from datetime import datetime

from tests.helpers.utils import sync_create_start_core_lib
from track_core_lib.data_layers.data.db.entities.exercise import Exercise


class TestTrackCoreLib(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.track_core_lib = sync_create_start_core_lib()

    def test_track(self):
        user_id = 1
        self.assertEqual(len(self.track_core_lib.exercise.all(user_id)), 0)
        self.track_core_lib.exercise.create(user_id, Exercise.ExerciseType.RUN, 1, datetime.utcnow())
        self.assertEqual(len(self.track_core_lib.exercise.all(user_id)), 1)
        first_id = self.track_core_lib.exercise.all(user_id)[0]['id']
        exercise = self.track_core_lib.exercise.get(first_id)
        self.assertNotEqual(exercise, None)
        self.assertEqual(exercise[Exercise.type.key], Exercise.ExerciseType.RUN.value)
