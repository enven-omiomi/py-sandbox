from unittest.mock import patch, MagicMock
import pytest

from src.fuga import Fuga


@pytest.fixture(scope="module")
def hoge_mock():
    with patch('src.hoge.Hoge') as mock:
        mock.say_hello.return_value = 'HELLO!'
        yield mock


def test_say_hello_goodbye():
    fuga = Fuga()
    assert fuga.say_hello_goodbye() == 'HELLO! Good Bye!'
