from src.hoge import Hoge


class Fuga:
    def __init__(self, hoge: Hoge = Hoge()):
        self.hoge = hoge

    def say_hello_goodbye(self):
        return self.hoge.say_hello() + ' Good Bye!'
