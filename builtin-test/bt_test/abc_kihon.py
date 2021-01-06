import abc


class MyMeta1(abc.ABC):
    """
    抽象基底クラスを実装するためにはabc.ABCを継承するか、
    """
    @abc.abstractmethod
    def my_func_a(self, arg_a: str):
        pass

    @classmethod
    @abc.abstractmethod
    def my_func_b(cls, arg_b: str):
        raise NotImplementedError()

    @staticmethod
    @abc.abstractmethod
    def my_func_c(arg_c: str):
        pass

class MyMeta2(metaclass=abc.ABCMeta):
    """
    metadata=abc.ABCMetaを指定する
    abc.ABC自体もmetaclassにABCMetaを指定している
        ↓
    class ABC(metaclass=ABCMeta): ...
    """
    @abc.abstractmethod
    def my_func_d(self, arg_d: str):
        pass

class Concrete_1(MyMeta2):
    pass

class Concrete_2(MyMeta2):

    def my_func_d(self, arg_d: str):
        print('%s %s' % (self.my_func_d.__name__, arg_d))

class Concrete_3(MyMeta2):

    def my_func_d(self, arg_dd: str):
        print('%s %s' % (self.my_func_d.__name__, arg_dd))


if __name__ == '__main__':
    # 抽象基底クラスのタイプはどちらの実装もABCMetaになる
    print(type(MyMeta1))  # <class 'abc.ABCMeta'>
    print(type(MyMeta2))  # <class 'abc.ABCMeta'>

    concrete = Concrete_2()
    print(type(concrete))
    concrete.my_func_d('fd')

    concrete = Concrete_3()
    print(type(concrete))
    concrete.my_func_d('fd')
