from abc import ABCMeta
from dataclasses import Field, dataclass, field, InitVar, fields, is_dataclass
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
from functools import wraps

def personal_info(**kwargs):
    return field(**kwargs, metadata={'personal_info': True})

def persondataclass(clazz):
    @wraps(clazz)
    def wrap(*args, **kwargs):
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

class DataclassMeta(metaclass=ABCMeta):
    bar: str = ''

    def __new__(cls, *args, **kwargs):
        dataclass(cls)
        return super().__new__(cls)

class DataclassImpl(DataclassMeta):
    foo: str = ''
    ### ↓を定義していると2回目以降のDataclassImplインスタンス生成時にエラーになる
    ### DataclassMetaの方で__new__の中で"if not is_dataclass(cls)"などして
    ### 2回以上dataclassが呼び出されないようにする必要がある
    # lis: list = field(default_factory=list)

@dataclass
class DataclassMeta2(metaclass=ABCMeta):
    bar: str = ''

class DataclassImpl2(DataclassMeta2):
    foo: str = ''

@dataclass
class DataclassMeta3(metaclass=ABCMeta):
    bar: str = ''

    def __new__(cls, *args, **kwargs):
        dataclass(cls)
        return super().__new__(cls)
class DataclassImpl3(DataclassMeta3):
    foo: str = ''

@dataclass
class DataclassSuper:
    bar: str = ''

    def __new__(cls):
        print('super 1: %s', cls.__name__)
        setattr(cls, '__test_attr__', ['super1'])
        print(object.__getattribute__(cls, '__test_attr__'))
        return super().__new__(cls)

class DataclassImpl4(DataclassSuper):
    foo: str = ''
    def __new__(cls):
        print('super 2: %s', cls.__name__)
        setattr(cls, '__test_attr__', ['super2'])
        print(object.__getattribute__(cls, '__test_attr__'))
        return super().__new__(cls)

class DataclassImpl5(DataclassImpl4):
    foo: str = ''
    def __new__(cls):
        print('super 3: %s', cls.__name__)
        # print(object.__getattribute__(cls, '__test_attr__'))
        return super().__new__(cls)

    def func_a(str):
        return None

# -----------------------------------------------------------------

if __name__ == '__main__':

    taro = CustomPerson('taro', 'tanaka', 20)
    print(taro.first_name)
    print(taro.last_name)
    print(taro.age)
    print(taro.personal_id)

    print('\n---------\n')

    dc_impl = DataclassImpl()
    print(dc_impl)
    print(is_dataclass(dc_impl))
    print(DataclassImpl(foo='fu'))

    print('\n---------\n')

    dc_impl_2 = DataclassImpl2()
    print(dc_impl_2)
    print(is_dataclass(dc_impl_2))
    print(DataclassImpl2(bar='ba'))

    print('\n---------\n')

    dc_impl_3 = DataclassImpl3()
    print(dc_impl_3)
    print(is_dataclass(dc_impl_3))
    print(DataclassImpl3(bar='ba', foo='fu'))

    print('\n---------\n')

    dc_impl_4 = DataclassImpl4()
    print(dc_impl_4)
    print(is_dataclass(dc_impl_4))
    dc_impl_5 = DataclassImpl5()
    print(dc_impl_5)
    print(is_dataclass(dc_impl_5))
    print(dc_impl_5.func_a.__dict__)
