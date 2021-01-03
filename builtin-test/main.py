from dataclasses import fields, field

from bt_test.dataclass_test import Person

if __name__ == '__main__':
    taro = Person('taro', 'tanaka', 20)
    print(taro.full_name())
