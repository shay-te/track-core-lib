import datetime

from core_lib.connection.mongodb_connection_registry import MongoDBConnectionRegistry
from core_lib.data_layers.data_access.data_access import DataAccess
from core_lib.error_handling.not_found_decorator import NotFoundErrorHandler

from track_core_lib.data_layers.data.mongodb.track_entry import TrackEntry
from track_core_lib.data_layers.data.track import TrackType


class TrackDataAccess(DataAccess):

    def __init__(self, db: MongoDBConnectionRegistry):
        self.mongodb = db

    @NotFoundErrorHandler()
    def get(self, user_id: int, year: int):
        with self.mongodb.get() as client:
            return client['track']['track'].find_one({'user_id': user_id, 'year': year})

    def create(self, user_id: int, created_at: datetime.datetime):
        with self.mongodb.get() as client:
            data = {
                'user_id': user_id,
                'year': created_at.year,
                'created_at': created_at.isoformat(),
                'entries': [],
                'entries_ids': []
            }
            client.track.track.insert_one(data)

    def register_entity(self, user_id: int, track_date: datetime.datetime, type: TrackType, meta_data: dict):
        with self.mongodb.get() as client:
            entry = TrackEntry(date=track_date, type=type.value, metadata=meta_data)
            # entry_data = dict(entry.__dict__)
            # entry_data['created_at'] = track_date
            entry_data = {
                'date': track_date,
                'type': type.value,
                'metadata': meta_data
            }
            return client.track.track.update_one({'user_id': user_id, 'year': track_date.year},
                                                   {'$push': {'entries': entry_data},
                                                    '$addToSet': {'entries_ids': entry.id}},
                                                   upsert=True)

    def all(self, user_id: int, type: TrackType = None):
        with self.mongodb.get() as client:
            query_id = {'user_id': user_id}
            if type:
                query_id['entries'] = {'$elemMatch': {'type': type.value}}
            documents = client.track.track.find(query_id)
            all_entries = []
            for document in documents:
                all_entries.extend(document.get('entries', []))
        return all_entries

    def count_user_document(self, user_id: int):
        with self.mongodb.get() as client:
            query_id = {'user_id': user_id}
            return client.track.track.count_documents(query_id)
