"""
具象クラスでabstractmethodを実装しないとエラーになるが、
引数に関しては同じでなくてもよい⇒Pythonの仕様

引数も合わせて軽傷を強制させるにはどうしたらいいかのテスト
"""

from abc import ABCMeta, abstractclassmethod
import inspect


class Foo(metaclass=ABCMeta):
    __require_arguments__ = {'a': str, 'b': str}

    def __new__(cls, *args, **kwargs):
        print('new: ' + cls.__name__)
        print(cls.mro())  # https://docs.python.org/ja/3/library/functions.html#super
        self = super().__new__(cls)  # self = 具象クラス のインスタンスオブジェクト
        func = object.__getattribute__(self, '__init__')  # Bar.__init__ の function object

        # https://docs.python.org/ja/3.9/library/inspect.html#inspect.getfullargspec
        arg_spec = inspect.getfullargspec(func)
        init_args = arg_spec.args
        print(init_args)

        # 具象クラスの__init__メソッドの引数に必要な引数が定義されているかのチェック
        if not all(reqiore_arg in init_args for reqiore_arg in cls.__require_arguments__.keys()):
            raise NotImplementedError('you have to implement required arguments to __init__: %s' % cls.__require_arguments__)

        # 引数の型情報
        arg_annotations: dict = arg_spec.annotations
        print(arg_annotations)
        for arg_, type_ in cls.__require_arguments__.items():
            if arg_annotations.get(arg_) is not type_:
                raise NotImplementedError('invalid type arguments on __init__: %s' % cls.__require_arguments__)

        print(type(self))
        return self

    @abstractclassmethod
    def __init__(self, a: str, b: str):
        pass

    @abstractclassmethod
    def say_foo(self):
        pass

    def __call__(self):
        print('called')

class Bur(Foo):
    # metaclassで定義されている__init__とは異なる引数でも問題なく実装できる
    def __init__(self, c):
        print('init bur')
        self.a = 'u'
        self.c = c

    def say_foo(self):
        print('foo ' + self.a)

class Bor(Foo):
    # metaclassで定義されている__init__とは異なる引数でも問題なく実装できる
    def __init__(self, a: str, b: int):
        print('init bor')
        self.a = a
        self.c = b

    def say_foo(self):
        print('foo ' + self.a)

class Bar(Foo):
    def __init__(self, a: str, b: str):
        print('init bar')
        self.a = a
        self.b = b

    def say_foo(self):
        print('foo ' + self.a)


if __name__ == '__main__':
    bar = Bar('a', 'b')
    bar.say_foo()

    print('-----------')

    try:
        bur = Bur('c')
    except BaseException as error:
        print(error)

    print('-----------')

    try:
        bor = Bor('a', 1)
    except BaseException as error:
        print(error)
