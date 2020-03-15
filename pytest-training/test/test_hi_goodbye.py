from unittest.mock import patch, MagicMock


class HogeMock:
    def say_hello(self):
        return 'Hi!'


with patch('src.hoge.Hoge', new_callable=MagicMock(return_value=HogeMock)):
    from src.fuga import Fuga

    def test_say_hello_goodbye():
        fuga = Fuga()
        assert fuga.say_hello_goodbye() == 'Hello! Good Bye!'
