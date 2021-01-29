from typing import List
from pydantic import BaseModel


class Foo(BaseModel):
    count: int
    size: float = None


class Bar(BaseModel):
    apple = 'x'
    banana = 'y'


class Spam(BaseModel):
    # モデルを型に指定すればより複雑な階層データ構造を表現できる
    foo: Foo
    bars: List[Bar]
