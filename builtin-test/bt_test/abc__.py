from abc import ABCMeta, abstractmethod

class Foo(metaclass=ABCMeta):
    """ 抽象クラス
    """
    @abstractmethod
    def __init__(self, a: str, b: str):
        pass

    @abstractmethod
    def func_a(self, c: int, d: list):
        pass

class Bar(Foo):
    """ 継承クラス
    """
    # 引数の数や型が違う
    def __init__(self, e: int, f: dict, g: list):
        print('init bar')
        self.a = e
        self.b = f

    # 引数名が違う
    def func_a(self, cccc: int, dddd: list):
        print('func_a')


if __name__ == '__main__':
    bar = Bar(1, {}, [])
    bar.func_a(1, 2)
