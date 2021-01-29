from pydantic.types import Json
import pytest
import json
from pydantic import ValidationError

from src.error_handling import Model, CustomErrorModel, CustomErrorModel2


def test_エラーハンドリング():
    data = dict(
        # 1. is_required 属性が初期値指定されていないのに未指定
        # 2. intのリストなのに文字列'bad'がある
        list_of_ints=['1', 2, 'bad'],
        # 3. floatじゃない
        a_float='not a float',
        # 4.
        recursive_model={'lat': 4.2, 'lng': 'New York'},
        # 5. 42以上のintじゃないとダメ
        gt_int=21,
    )
    with pytest.raises(ValidationError) as err:
        Model(**data)

    # ValidationError を取り出す
    val_error = err.value
    # エラー結果の情報をリストで受け取る
    err_info = val_error.errors()

    # 'errors()'で取得したlocはタプル
    # json()からjson.loads()したlocはリスト という違いがある

    # エラー要因のリストはクラス変数の定義順に出てるみたい
    assert err_info[0]['loc'] == ('is_required',)
    assert err_info[0]['msg'] == 'field required'
    assert err_info[0]['type'] == 'value_error.missing'

    assert err_info[1]['loc'] == ('gt_int',)
    assert err_info[1]['msg'] == 'ensure this value is greater than 42'
    assert err_info[1]['type'] == 'value_error.number.not_gt'
    # ctx: errorの表示に必要な値を含むオプションオブジェクト
    assert err_info[1]['ctx'] == {"limit_value": 42}

    # クラス変数名と、リスト内の要素数（0から始まるので3つ目の要素）
    # がlocに含まれている
    assert err_info[2]['loc'] == ('list_of_ints', 2)
    assert err_info[2]['msg'] == 'value is not a valid integer'
    assert err_info[2]['type'] == 'type_error.integer'

    assert err_info[3]['loc'] == ('a_float',)
    assert err_info[3]['msg'] == 'value is not a valid float'
    assert err_info[3]['type'] == 'type_error.float'

    # Locationモデルのどの要素に誤りがあるか、要素名が含まれる(lng)
    assert err_info[4]['loc'] == ('recursive_model', 'lng')
    assert err_info[4]['msg'] == 'value is not a valid float'
    assert err_info[4]['type'] == 'type_error.float'

    # json文字列を抜き出す
    err_info_from_json = json.loads(val_error.json())

    assert err_info_from_json[0]['loc'] == ['is_required']
    assert err_info_from_json[0]['msg'] == 'field required'
    assert err_info_from_json[0]['type'] == 'value_error.missing'

    assert err_info_from_json[1]['loc'] == ['gt_int']
    assert err_info_from_json[1]['msg'] == 'ensure this value is greater than 42'
    assert err_info_from_json[1]['type'] == 'value_error.number.not_gt'
    # ctx: errorの表示に必要な値を含むオプションオブジェクト
    assert err_info_from_json[1]['ctx'] == {"limit_value": 42}

    # クラス変数名と、リスト内の要素数（0から始まるので3つ目の要素）
    # がlocに含まれている
    assert err_info_from_json[2]['loc'] == ['list_of_ints', 2]
    assert err_info_from_json[2]['msg'] == 'value is not a valid integer'
    assert err_info_from_json[2]['type'] == 'type_error.integer'

    assert err_info_from_json[3]['loc'] == ['a_float']
    assert err_info_from_json[3]['msg'] == 'value is not a valid float'
    assert err_info_from_json[3]['type'] == 'type_error.float'

    # Locationモデルのどの要素に誤りがあるか、要素名が含まれる(lng)
    assert err_info_from_json[4]['loc'] == ['recursive_model', 'lng']
    assert err_info_from_json[4]['msg'] == 'value is not a valid float'
    assert err_info_from_json[4]['type'] == 'type_error.float'

    # human readableなエラー表現を出力
    print(str(val_error))

def test_custom_errors():
    with pytest.raises(ValidationError) as err:
        CustomErrorModel(foo='ber')

    val_error = err.value
    error_info = val_error.errors()
    assert error_info[0]['loc'] == tuple(['foo'])
    # ValueError()のmessageがそのまま入る
    assert error_info[0]['msg'] == 'value must be "bar"'
    assert error_info[0]['type'] == 'value_error'

    with pytest.raises(ValidationError) as err:
        CustomErrorModel2(foo='ber')

    val_error = err.value
    error_info = val_error.errors()
    assert error_info[0]['loc'] == tuple(['foo'])
    # カスタムエラーで定義したメッセージ
    assert error_info[0]['msg'] == 'value is not \"bar\", got \"ber\"'
    # カスタムエラーのcodeに定義したtype
    assert error_info[0]['type'] == 'value_error.not_a_bar'
