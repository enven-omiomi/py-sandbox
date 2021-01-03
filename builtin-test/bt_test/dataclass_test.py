from dataclasses import Field, dataclass, field, InitVar, fields
from typing import Any

@dataclass()
class Person():
    first_name: str = ''
    last_name: str = ''
    age: int = 0
    full_name: str = field(init=False)
    separater: InitVar[str] = None

    def __post_init__(self, separater):
        _separater = separater if separater is not None else ' '
        self.full_name = _separater.join(
                [self.first_name, self.last_name])

# データクラスを使わないで定義したパターン
class Person_():
    def __init__(self, first_name: str = '', last_name: str = '', age: int = 0) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

# -----------------------------------------------------------------

# デコレータを自作するテスト

def frozendataclass(clazz):
    def wrap(clazz):
        setattr(clazz, 'music', 'let it go')
        return dataclass(clazz, eq=False ,frozen=False, unsafe_hash=True)

    return wrap(clazz)

@frozendataclass
class FrozenPerson():
    first_name: str = ''
    last_name: str = ''
    age: int = 0

# -----------------------------------------------------------------

# field()の自作と__getattribute__の改造

import uuid

def personal_info(**kwargs):
    return field(**kwargs, metadata={'personal_info': True})

def persondataclass(clazz):
    def wrap(clazz):
        def _get_attribute(self, name: str) -> Any:
            # 再帰を防ぐためにobjectのgetattributeを使う
            dc_fields: dict = object.__getattribute__(
                self, '__dataclass_fields__')

            field_: Field = dc_fields.get(name)
            if field_ and field_.metadata.get('personal_info'):
                return '###'

            return object.__getattribute__(self, name)

        setattr(clazz, 'personal_id', uuid.uuid4())
        setattr(clazz, '__getattribute__', _get_attribute)
        return dataclass(clazz)

    return wrap(clazz)

@persondataclass
class CustomPerson():
    first_name: str = personal_info(default='')
    last_name: str = personal_info(default='')
    age: int = 0

# -----------------------------------------------------------------


if __name__ == '__main__':
    foo = Foo('fuu', 'bar')
    print(foo.foo)
    print(foo.bar)

    print('\n---------\n')

    taro = CustomPerson('taro', 'tanaka', 20)
    print(taro.first_name)
    print(taro.last_name)
    print(taro.age)
    print(taro.personal_id)
