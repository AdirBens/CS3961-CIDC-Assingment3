import json

from Common import Exceptions
from Common.Exceptions import ResourceNotFound


class DataBase(object):
    """
    An abstraction of DataBase, provides safe, convenient and robust interface to handle collections.
    """
    def __init__(self):
        self._STORAGE = dict()
        self._RESOLVER = dict()
        self._ID = 0

    def insert_record(self, record, force_id: int | None = None) -> int:
        if record["name"] in self._RESOLVER:
            raise Exceptions.ResourceAlreadyExists()

        record_id = self._generate_id() if force_id is None else force_id
        record["ID"] = record_id

        self._RESOLVER[record["name"]] = record["ID"]
        self._STORAGE[record_id] = record

        return record_id

    def fetch_record(self, record_name: str = None, record_id: int = None) -> json:
        if record_id is None:
            record_id = self._resolve_id_by_name(record_name)

        try:
            return self._STORAGE[record_id]
        except KeyError:
            raise ResourceNotFound()

    def fetch_all(self) -> json:
        all_records = dict(sorted([(record_id, record) for record_id, record
                                   in self._STORAGE.items() if isinstance(record_id, int)]))

        return all_records

    def delete_record(self, record_name: str = None, record_id: int = None) -> json:
        if record_id is None:
            record_id = self._resolve_id_by_name(record_name)
            self._RESOLVER.pop(record_name)

        elif record_name is None:
            record_name = self._resolve_name_by_id(record_id)
            self._RESOLVER.pop(record_name)

        try:
            return self._STORAGE.pop(record_id)
        except KeyError:
            raise ResourceNotFound()

    def replace_record(self, record_id: int, new_record) -> int:
        try:
            new_record["ID"] = record_id
            self._STORAGE[record_id] = new_record
            return record_id

        except KeyError:
            raise ResourceNotFound()

    def _generate_id(self) -> int:
        self._ID += 1
        return self._ID

    def _resolve_id_by_name(self, name: str) -> int:
        try:
            return self._RESOLVER[name]

        except KeyError:
            raise ResourceNotFound()

    def _resolve_name_by_id(self, id: int) -> str:
        try:
            return self._STORAGE[id]["name"]

        except KeyError:
            raise ResourceNotFound()