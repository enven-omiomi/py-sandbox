from pydantic.types import Json
import pytest
import json
from pydantic import ValidationError

from src.recursive_model import Bar, Foo, Spam



def test_再帰モデル():
    # コンストラクタの引数はDict型でよい (FooとかBarとかを初期化する必要がない)
    m = Spam(foo={'count': 4}, bars=[{'apple': 'x1'}, {'apple': 'x2'}])
    assert m.foo == Foo(count=4)
    assert m.bars[0] == Bar(apple='x1')
    assert m.bars[1] == Bar(apple='x2')
    assert m.dict() == {
        'foo': {'count': 4, 'size': None},
        'bars': [
            {'apple': 'x1', 'banana': 'y'},
            {'apple': 'x2', 'banana': 'y'},
        ]
    }
