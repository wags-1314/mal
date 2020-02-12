import reader as reader
import printer as printer
import lisp_types as types


def READ(string: str) -> types.LispType:
    return reader.read_string(string)


def EVAL(expr: types.LispType) -> types.LispType:
    return expr


def PRINT(expr: types.LispType) -> str:
    return printer.print_string(expr)


def REP(expr: str) -> str:
    return PRINT(EVAL(READ(expr)))


if __name__ == '__main__':
    while True:
        try:
            print(REP(input('user> ')))
        except Exception as e:
            print(e)