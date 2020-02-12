import reader
import printer


def READ(string: str):
    return reader.read_string(str)


def EVAL(expr):
    return expr


def PRINT(expr):
    return printer.print_string(reader)


def REP(expr):
    return PRINT(EVAL(READ(expr)))


if __name__ == '__main__':
    print(REP(input('user> ')))

