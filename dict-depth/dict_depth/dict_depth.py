from collections.abc import Mapping, Iterable
from typing import Any, Dict

def dict_depth(d):
    if isinstance(d, dict):
        return 1 + (max(map(dict_depth, d.values())) if d else 0)
    return 0

def mask_elm(obj: dict):
    def _mask(obj_):
        return '###'

    if isinstance(obj, Mapping):
        return {name: mask_elm(value) for name, value in obj.items()}
    elif isinstance(obj, tuple):
        return tuple([mask_elm(elm) for elm in obj])
    elif isinstance(obj, list):
        return [mask_elm(elm) for elm in obj]
    elif isinstance(obj, set):
        return set([mask_elm(elm) for elm in obj])
    else:
        return _mask(obj)


# def mask_dict(dct: dict, depth: int = 1):
#     def depth_(obj):
#         if isinstance(obj, Mapping):
#             num = 1 + (max(map(depth_, obj.values())) if obj else 0)
#             if num == depth:
#                 map(mask, obj.values())
#             return num
#         return 0
#     depth_(dct)
#     return dct
