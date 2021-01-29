from typing import List
from pydantic import BaseModel, ValidationError, conint, validator, \
    PydanticValueError


class Location(BaseModel):
    lat = 0.1
    lng = 10.1


class Model(BaseModel):
    is_required: float
    gt_int: conint(gt=42)  # 制約付きint
    list_of_ints: List[int] = None
    a_float: float = None
    recursive_model: Location = None

class CustomErrorModel(BaseModel):
    foo: str

    @validator('foo')
    def name_must_contain_space(cls, v):
        # クラスメソッドで細かいバリデーション条件を指定できる
        if v != 'bar':
            raise ValueError('value must be "bar"')

        return v

class NotABarError(PydanticValueError):
    # 独自のエラー定義
    # code: errors()のtype
    # msg_template: errors()のmsgに渡す値のテンプレート
    # wrong_value: このエラーのインスタンス生成時にkw引数で渡す
    # wrong_valueという名称はPydanticValueErrorに定義されているわけではないので、
    # 自由に定義できる
    code = 'not_a_bar'
    msg_template = 'value is not "bar", got "{wrong_value}"'

    # PydanticValueErrorのほかにもMissingError,
    # PydanticTypeErrorなどあるので、いろいろ定義する必要がありそう

class CustomErrorModel2(BaseModel):
    foo: str

    @validator('foo')
    def name_must_contain_space(cls, v):
        # クラスメソッドで細かいバリデーション条件を指定できる
        if v != 'bar':
            raise NotABarError(wrong_value=v)

        return v
