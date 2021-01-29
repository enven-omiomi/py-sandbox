from pydantic.types import Json
import pytest
import json
from pydantic import ValidationError

from src.basic import User


def test_基本形():
    # キーワード引数でフィールドを指定する
    # strで数字を指定しても良い感じに変換してくれる
    user = User(id='123')
    assert user.id == 123
    assert type(user.id) == int

    # 初期値が設定されているので登録されている
    assert user.name == 'Jane Doe'
    # 初期化時にnameを指定しなかったのでフィールドに含まれない
    assert user.__fields_set__ == {'id'}

    user = User(id='123', name='tanaka')
    assert user.id == 123
    assert user.name == 'tanaka'
    # 初期化時にnameを指定したのでフィールドに含まれる
    assert user.__fields_set__ == {'id', 'name'}

    # dictに変換できる関数が作成される
    assert user.dict() == dict(user) == {'id': 123, 'name': 'tanaka'}

    # 基本的にミュータブル
    user.id= 321
    assert user.id == 321

    # 異なるtypeを指定しるとValidationError
    with pytest.raises(ValidationError):
        User(id='abc')

def test_メソッドと属性():
    user = User(id=123)

    # dict()
    assert user.dict() == dict(user) == {'id': 123, 'name': 'Jane Doe'}

    # json()
    assert user.json() ==  json.dumps({'id': 123, 'name': 'Jane Doe'}) \
        == '{"id": 123, "name": "Jane Doe"}'

    # copy()
    copy_user = user.copy()
    # 比較はイコール
    assert copy_user == user
    # 別のインスタンス
    assert copy_user is not user
    copy_user.id == 321
    assert user.id == 123

    # parse_obj()
    # dictを引数にインスタンスを生成
    # 引数がdictなこと以外は__init__とほぼ同じ
    user = User.parse_obj({'id': 123, 'name': 'James'})
    assert user.id == 123
    assert user.name == 'James'

    # parse_raw()
    # strまたはbyteを受け取ってjsonとして解析してから
    # parse_obj()に値を渡す
    user = User.parse_raw('{"id": 123, "name": "James"}')
    assert user.id == 123
    assert user.name == 'James'

    # parse_file()
    # ファイルから読み込んでparse_objに渡す
