from dataclasses import dataclass

class Foo:
    foo: str
    def __init__(self, foo):
        self.foo = foo

    def format(self):
        return self.foo.upper()

class Bar(Foo):
    bar: str
    


if __name__ == '__main__':
    foo_ = Foo('fuu')
    print(foo_.format())
    print(foo_.__dict__)
    foo_.__dict__['foo'] = 'bar'
    print(foo_.__dict__)
    print(foo_.format())

    # # エラーにはならない
    # foo_.__dict__ = {}
    # print(foo_.__dict__)
    # # クラス変数"foo"が消えるのでここでエラーになる
    # print(foo_.format())

    # 出力される要素の順序は異なるが内容は一緒
    print(foo_.__dir__())
    print(dir(foo_))

    print(dir())
    print(dir(Foo))
