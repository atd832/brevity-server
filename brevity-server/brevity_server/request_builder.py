
class RequestBuilder:
    def __init__(self):
        self.req = ''

    def append(self, s: str):
        self.req = self.req.strip()
        self.req += ' ' + s
        return self

    def header(self, h: str):
        n = h.upper() + ' ' + self.req
        self.req = n
        return self

    def __str__(self):
        return str(self.req)

