class BaseController:
    def __init__(self):
        self._items = {}

    def exists(self, item_id):
        return item_id in self._items

    def get(self, item_id):
        return self._items.get(item_id)

    def get_all(self):
        return list(self._items.values())

    def remove(self, item_id):
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False