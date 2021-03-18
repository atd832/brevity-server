from json import dumps


class Request:
    def __init__(self, key: str, data: dict):
        self.key = key
        self.data = data
        self.request = dumps({key: data})

    def __str__(self):
        return self.request



