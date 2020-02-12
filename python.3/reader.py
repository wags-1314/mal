import re
import lisp_types as types
from typing import List, Optional, Callable


def escape(string: str) -> str:
    return string.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')

class Reader:
    def __init__(self, tokens) -> None:
        self.tokens: List[str] = tokens
        self.count: int = 0

    def is_at_end(self) -> bool:
        if self.count >= len(self.tokens):
            return True
        else:
            return False

    def next(self) -> Optional[str]:
        if self.is_at_end():
            return None
        else:
            self.count += 1
            return self.tokens[self.count - 1]

    def peek(self) -> Optional[str]:
        if self.is_at_end():
            return None
        else:
            return self.tokens[self.count]


def tokenize(string: str) -> List[str]:
    tre = re.compile(r"""[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)""");
    return [token for token in re.findall(tre, string) if token[0] != ';']


def read_list(
        reader: Reader,
        stop: str=')',
        seq: Callable[[list], types.LispType]=types.make_list
    ) -> types.LispType:
    reader.next()
    lst = []

    token = reader.peek()
    while token != stop:
        if token is None:
            raise types.LispException('unbalanced list')

        lst.append(read_form(reader))
        token = reader.peek()
    reader.next()

    return seq(lst)


def read_atom(reader: Reader) -> types.LispType:
    token = reader.next()
    if re.match(r'^[-+]?\d+$', token):
        return int(token)
    elif re.match(r'^"(?:[\\].|[^\\"])*"$', token):
        return escape(token[1:-1])
    elif token[0] == '"':
        raise types.LispException('unbalanced \'"\'')
    elif token[0] == ':':
        return types.KeyWord(token[1:])
    elif token == 'nil':
        return None
    elif token == 'true':
        return True
    elif token == 'false':
        return False
    else:
        return types.Symbol(token)


def read_form(reader: Reader) -> types.LispType:
    token = reader.peek()

    if token == '(':
        return read_list(reader)
    elif token == '[':
        return read_list(reader, stop=']', seq=types.make_vector)
    elif token == '{':
        return read_list(reader, stop='}', seq=types.make_hash_map)
    elif token == '\'':
        reader.next()
        return types.make_list([types.Symbol('quote'), read_form(reader)])
    elif token == '`':
        reader.next()
        return types.make_list([types.Symbol('quasiquote'), read_form(reader)])
    elif token == '~':
        reader.next()
        return types.make_list([types.Symbol('unquote'), read_form(reader)])
    elif token == '~@':
        reader.next()
        return types.make_list([types.Symbol('splice-unquote'), read_form(reader)])
    elif token == '@':
        reader.next()
        return types.make_list([types.Symbol('deref'), read_form(reader)])
    elif token == '^':
        reader.next()
        meta = read_form(reader)
        return types.make_list([types.Symbol('with-meta'), read_form(reader), meta])
    else:
        return read_atom(reader)


def read_string(string: str) -> types.LispType:
    tokens = tokenize(string)
    reader = Reader(tokens)
    return read_form(reader)


if __name__ == '__main__':
    while True:
        print(read_string(input('> ')))