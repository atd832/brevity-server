from brevity_server.request import Request
from json import dumps


class TestRequest:

    def test_request(self):
        s = Request('test', {})
        expected = dumps({'test': {}})

        assert str(s) == expected
