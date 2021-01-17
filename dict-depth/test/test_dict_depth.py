import pytest
from dict_depth.dict_depth import mask_elm, mask_dict

TEST_DICT = {
    "a5": "a",
    "b5": {
        "a4": "a",
        "b4": {
            "a3": {
                "a2": "a",
                "b2": {
                    "a1": "a",
                    "b1": ["a", "b"],
                    "c1": ("a", "b"),
                    "d1": {"a", "b"},
                    "e1": "a",
                },
                "c2": "c"
            },
            "b3": "b"
        },
        "c4": "a",
        "d4": {
            "a3": {
                "a2": "a"
            },
            "b3": "b"
        }
    },
    "c5": {"a", "b", "c"},
    "d5": ("d", "d", "d"),
}

def test_mask_elm():
    # tuple
    tuple_obj = (1, '2', True)
    masked = mask_elm(tuple_obj)
    assert masked == ('###', '###', '###')
    tuple_obj = (1, '2', True, ('a', 'b'))
    masked = mask_elm(tuple_obj)
    assert masked == ('###', '###', '###', ('###', '###'))

    # list
    list_obj = [1, '2', True]
    masked = mask_elm(list_obj)
    assert masked == ['###', '###', '###']
    list_obj = [1, '2', True, ['a', 'b']]
    masked = mask_elm(list_obj)
    assert masked == ['###', '###', '###', ['###', '###']]

    # set
    sat_obj = {1, '2', True}
    masked = mask_elm(sat_obj)
    assert masked == {'###'}

    # dict
    masked = mask_elm(TEST_DICT)
    assert masked == {
        "a5": "###",
        "b5": {
            "a4": "###",
            "b4": {
                "a3": {
                    "a2": "###",
                    "b2": {
                        "a1": "###",
                        "b1": ["###", "###"],
                        "c1": ("###", "###"),
                        "d1": {"###", "###"},
                        "e1": "###",
                    },
                    "c2": "###"
                },
                "b3": "###"
            },
            "c4": "###",
            "d4": {
                "a3": {
                    "a2": "###"
                },
                "b3": "###"
            }
        },
        "c5": {"###", "###", "###"},
        "d5": ("###", "###", "###"),
    }
