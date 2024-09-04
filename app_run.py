from datetime import timedelta, datetime
from http import HTTPStatus

import hydra
import logging

from flask import Flask, request

from admin_core_lib_instance import TrackCoreLibInstance
from core_lib.web_helpers.request_response_helpers import response_json, request_body_dict
from core_lib.web_helpers.web_helprs_utils import WebHelpersUtils

from track_core_lib.data_layers.data.db.entities.exercise import Exercise

logger = logging.getLogger(__name__)


@hydra.main(config_path='config', config_name='app_config')
def main(cfg):
    WebHelpersUtils.init(WebHelpersUtils.ServerType.DJANGO)
    track_core_lib = TrackCoreLibInstance.init(cfg)
    app = Flask(__name__)
    app.debug = True

    @app.route('/api/exercise/all', methods=['GET'])
    def all():
        user_id = 1  # request.environ['user'].u_id # get from session
        return response_json({'exercises': track_core_lib.exercise.all(user_id)})

    @app.route('/api/exercise/<int:exercise_id>', methods=['GET'])
    def get(exercise_id):
        return response_json(track_core_lib.exercise.get(exercise_id))

    @app.route('/api/exercise/<int:exercise_id>', methods=['PUT'])
    def update(exercise_id):
        return response_json(track_core_lib.exercise.update(exercise_id, request_body_dict(request)))

    @app.route('/api/exercise', methods=['POST'])
    def create():
        user_id = 1  # request.environ['user'].u_id # get from session
        data = request_body_dict(request)
        type = data.get('type')
        duration_minutes = data.get('duration_minutes')
        start_datetime_str = data.get('start_datetime')
        assert type and duration_minutes and start_datetime_str

        datetime_str_fixed = start_datetime_str.replace('Z', '+00:00')
        start_datetime = datetime.fromisoformat(datetime_str_fixed)

        track = track_core_lib.exercise.create(user_id, Exercise.ExerciseType(type), duration_minutes, start_datetime)
        return response_json(track, status=HTTPStatus.CREATED)

    app.run(host=cfg.flask.host, port=cfg.flask.port)


if __name__ == '__main__':
    main()
