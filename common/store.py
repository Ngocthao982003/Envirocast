import json
from copy import copy
from typing import Union

from ..utils import startup


class AbstractStoreItem:

    namespace: str = ""

    def __init__(self, id: str) -> None:
        self.id = id

    def export(self, filepath: str):
        file = open(filepath, "w")
        data = self.get_dict()
        json.dump(data, file, indent=4)
        file.close()

    def get_dict(self) -> dict:
        raise NotImplementedError


class AbstractNamespace:

    def __init__(self, filepath: str, namespace: str) -> None:
        self._item_index: dict[str, AbstractStoreItem] = {}
        self.changes = False
        self.filepath = filepath
        self.namespace = namespace
        self.load(self.filepath)

    def get_by_id(self, item_id: str) -> Union[AbstractStoreItem, None]:
        item = self._item_index.get(item_id)
        if item:
            return copy(item)
        return None

    def get_by_name(self, item_name: str) -> list[AbstractStoreItem]:
        items = [
            copy(item) for item in self._item_index.values() if item.name == item_name
        ]
        return items

    def add(self, item: AbstractStoreItem):
        self._item_index[item.id] = item
        item.namespace = self.namespace
        self.changes = True
        self.store()

    def remove(self, item_id: str):
        del self._item_index[item_id]
        self.changes = True

    def load(self, filepath: str):
        raise NotImplementedError

    def store(self):
        raise NotImplementedError

    def verify_namespace(self, data: dict) -> bool:
        raise NotImplementedError


class AbstractStore:

    namespace: dict[str, AbstractNamespace] = {}
    _item_index: dict[str, AbstractStoreItem] = {}

    def __init__(self) -> None:
        startup.add_callback(self._load_user_namespace)

    def get_all(self):
        return self._item_index.values()

    def get_by_id(self, item_id: str):
        item = self._item_index.get(item_id)
        if item:
            return copy(item)
        return None

    def get_by_name(self, item_name: str) -> list[AbstractStoreItem]:
        items = [
            copy(item) for item in self._item_index.values() if item.name == item_name
        ]
        return items

    def add(self, namespace: str, item: AbstractStoreItem):
        item_namespace = self.namespace.get(namespace)
        if item_namespace:
            item_namespace.add(item)
            self._item_index[item.id] = item
        else:
            print(f"Envirocast: Namespace: {namespace} not found.")

    def remove(self, item_id: str):
        item = self._item_index.get(item_id)
        if item:
            namespace = self.namespace.get(item.namespace)
            if namespace:
                namespace.remove(item_id)
            del self._item_index[item_id]

    def update(self, item: AbstractStoreItem):
        raise NotImplementedError

    def load(self, filepath: str, namespace: str):
        raise NotImplementedError

    def merge(self, filepath: str, namespace: str):
        raise NotImplementedError

    def _load_user_namespace(self):
        raise NotImplementedError

    def unload(self, namespace: str):
        item_namespace = self.namespace.get(namespace)

        if item_namespace:
            for item in item_namespace._item_index:
                del self._item_index[item]
            del self.namespace[namespace]

    def store(self):
        for namespace in self.namespace.values():
            namespace.store()
