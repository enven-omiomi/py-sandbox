"""
具象クラスでabstractmethodを実装しないとエラーになるが、
引数に関しては同じでなくてもよい⇒Pythonの仕様

引数も合わせて軽傷を強制させるにはどうしたらいいかのテスト
"""

from abc import ABC, ABCMeta, abstractmethod
import inspect


class Foo(metaclass=ABCMeta):
    __require_arguments__ = {'a': str, 'b': str}

    def __new__(cls, *args, **kwargs):
        print('new: ' + cls.__name__)
        print(cls.mro())  # https://docs.python.org/ja/3/library/functions.html#super

        func = object.__getattribute__(cls, '__init__')  # Bar.__init__ の function object
        # 下の書き方でもOK
        # func = cls.__init__

        # https://docs.python.org/ja/3.9/library/inspect.html#inspect.getfullargspec
        arg_spec = inspect.getfullargspec(func)
        print(arg_spec)
        init_args = arg_spec.args
        # def __init__(self, a: str, b: str, *args, **kwargs): と書いた場合
        # argsとkwargsはinspect.getfullargspec(func).argsに含まれない
        # args = ['self', 'a', 'b']
        # 他の要素に含まれてる
        # FullArgSpec(args=['self', 'a', 'b'], varargs='args', varkw='kwargs', defaults=None,
        #             kwonlyargs=[], kwonlydefaults=None, annotations={'a': <class 'str'>, 'b': <class 'str'>})

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

        self = super().__new__(cls)  # self = 具象クラス のインスタンスオブジェクト
        print(type(self))
        return self

    @abstractmethod
    def __init__(self, a: str, b: str):
        pass

    @abstractmethod
    def func_a(self, c: int, d: list):
        pass


class Bur(Foo):
    # metaclassで定義されている__init__とは異なる引数でも問題なく実装できる
    def __init__(self, c):
        print('init bur')
        self.a = 'u'
        self.c = c

    def func_a(self):
        print('func_a')

class Bor(Foo):
    # metaclassで定義されている__init__とは異なる引数でも問題なく実装できる
    def __init__(self, a: str, b: int):
        print('init bor')
        self.a = a
        self.c = b

    def func_a(self):
        print('func_a')

class Bar(Foo):
    def __init__(self, a: str, b: str, *args, **kwargs):  # argsとkwargsはinspect.getfullargspec(func).argsに含まれない
        print('init bar')
        self.a = a
        self.b = b

    def func_a(self, c: int, d: list):
        print('func_a')

# ---------------------------------------------------

from functools import wraps

class InitDeco(metaclass=ABCMeta):
    """
    継承クラスの__init__の前後にabstractmethodを実行させたい
    """
    def __new__(cls, *args, **kwargs):
        cls.__init__ = cls.wrap_init(cls.__init__, cls.ante_init, cls.post_init)
        return super().__new__(cls)

    def wrap_init(func, ante_, post_):
        @wraps(func)
        def wrap(*args, **kwargs):
            ante_(*args, **kwargs)
            result = func(*args, **kwargs)
            post_(*args, **kwargs)
            return result
        return wrap

    @abstractmethod
    def ante_init(self):
        """
        init前の処理
        """
        pass

    @abstractmethod
    def post_init(self):
        """
        init後の処理
        """
        pass

class SubDeco(InitDeco):

    def __init__(slef):
        print('init')

    def ante_init(self):
        print('ante')

    def post_init(self):
        print('post')

if __name__ == '__main__':

    sub = SubDeco()

    bar = Bar('a', 'b')
    bar.func_a(0, [])

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
