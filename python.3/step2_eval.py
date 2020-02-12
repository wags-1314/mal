import reader as reader
import printer as printer
import lisp_types as types
from typing import Mapping, Callable

repl_env: Mapping[types.Symbol, Callable] = {
    types.Symbol('+'): lambda a, b: a + b,
    types.Symbol('-'): lambda a, b: a - b,
    types.Symbol('*'): lambda a, b: a * b,
    types.Symbol('/'): lambda a, b: int(a / b),
}


def READ(string: str) -> types.LispType:
    return reader.read_string(string)


def eval_ast(expr: types.LispType, env: Mapping) -> types.LispType:
    if types.is_symbol(expr):
        return env[expr]
    elif types.is_list(expr):
        return types.List([EVAL(e, env) for e in expr])
    elif types.is_vector(expr):
        return types.Vector([EVAL(e, env) for e in expr])
    elif types.is_hash_map(expr):
        return types.HashMap({x: EVAL(y, env) for x, y in expr.items()})
    else:
        return expr


def EVAL(expr: types.LispType, env: Mapping) -> types.LispType:
    if not types.is_list(expr):
        return eval_ast(expr, env)

    if len(expr) == 0:
        return expr

    evaled = eval_ast(expr, env)
    if type(evaled[0]) == Callable:
        fn, *args
    return fun(*args)


def PRINT(expr: types.LispType) -> str:
    return printer.print_string(expr)


def REP(expr: str) -> str:
    return PRINT(EVAL(READ(expr), repl_env))


if __name__ == '__main__':
    while True:
        try:
            print(REP(input('user> ')))
        except Exception as e:
            print(e)
