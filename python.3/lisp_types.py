from typing import Union, Any


class List(list):
    pass


class Symbol(str):
    pass


class KeyWord(str):
    def __repr__(self):
        return ':' + str.__repr__(self)[1: -1]

    def __str__(self):
        return self.__repr__()


class Vector(list):
    pass


class HashMap(dict):
    pass


class LispException(Exception):
    pass

LispType = Union[
    List, Symbol, int, bool, None, str, KeyWord, Vector,
    HashMap,
]


def is_list(obj: Any) -> bool:
    return type(obj) == List


def is_symbol(obj: Any) -> bool:
    return type(obj) == Symbol


def is_string(obj: Any) -> bool:
    return type(obj) == str


def is_vector(obj: Any) -> bool:
    return type(obj) == Vector


def is_hash_map(obj: Any) -> bool:
    return type(obj) == HashMap


def is_sequence(obj: Any) -> bool:
    return is_list(obj) or is_vector(obj)


def make_list(lst: list) -> List:
    return List(lst)


def make_vector(lst: list) -> Vector:
    return Vector(lst)


def make_hash_map(key_values: list) -> HashMap:
    keys = key_values[::2]
    values = key_values[1::2]
    if len(keys) == len(values):
        return HashMap({x: y for x, y in zip(keys, values)})
    else:
        raise Exception('no. of keys and values are not matching')