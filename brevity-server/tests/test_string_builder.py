from brevity_server.string_builder import StringBuilder


class TestStringBuilder:

    def test_string_builder(self):
        s = StringBuilder()
        s.header('header')
        s.append('test')

        assert s.val == 'HEADER test'