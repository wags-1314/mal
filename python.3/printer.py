import lisp_types as types


def escape(string: str) -> str:
    return string.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')


def print_string(expr: types.LispType, prnt_rd=True) -> str:
    if types.is_list(expr):
        return '({})'.format(
            ' '.join([print_string(e) for e in expr])
        )
    elif types.is_vector(expr):
        return '[{}]'.format(
            ' '.join([print_string(e) for e in expr])
        )
    elif types.is_hash_map(expr):
        lst = []
        for  key, value in expr.items():
            lst.append(print_string(key))
            lst.append(print_string(value))

        return f'{{{" ".join(lst)}}}'
    elif expr is None:
        return 'nil'
    elif expr is True:
        return 'true'
    elif expr is False:
        return 'false'
    elif types.is_string(expr):
        if prnt_rd:
            return '"' + escape(expr) + '"'
        else:
            return '"' + expr + '"'
    else:
        return str(expr)
