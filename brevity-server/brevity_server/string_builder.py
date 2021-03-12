
class StringBuilder:
    def __init__(self):
        self.val = ''

    def append(self, s: str):
        self.val = self.val.strip()
        self.val += ' ' + s
        return self

    def header(self, h: str):
        n = h.upper() + ' ' + self.val
        self.val = n
        return self

