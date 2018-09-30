from ply import yacc
from ply import lex
import argparse

tokens = [
    "YARN",
    "NUMBR",
    "NUMBAR",
    "TROOF",
    "TYPE",

    "NAME",
    "OF",
    "AN",
    "VAR",
    "ITZ",

    "IF_START",
    "IF_YES",
    "IF_NO",
    "IF_END",

    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "EQUALS",
    "MOD",
    "MAX",
    "MIN",

    "CHANGE_TYPE",
    "NEWLINE",

    "PRINT",
    "INPUT",

    # logic
    "LOGIC_EQUALS",
    "LOGIC_DIFFER",
    "LOGIC_AND",
    "LOGIC_OR",
    "LOGIC_XOR",

    "LOGIC_NOT",
    "LOGIC_ALL",
    "LOGIC_ANY",
    "LOGIC_END",
]


def t_LOGIC_AND(t):
    r'BOTH\ OF'
    return t


def t_LOGIC_OR(t):
    r'EITHER\ OF'
    return t


def t_LOGIC_XOR(t):
    r'WON\ OF'
    return t


def t_LOGIC_NOT(t):
    r'NOT\ OF'
    return t


def t_LOGIC_ALL(t):
    r'ALL\ OF'
    return t


def t_LOGIC_ANY(t):
    r'ANY\ OF'
    return t


def t_LOGIC_END(t):
    r'MKAY'
    return t


def t_LOGIC_EQUALS(t):
    r'BOTH\ SAEM'
    return t


def t_LOGIC_DIFFER(t):
    r'DIFFRINT'
    return t


def t_IF_START(t):
    r'O\ RLY\?'
    return t


def t_IF_YES(t):
    r'YA\ RLY'
    return t


def t_IF_NO(t):
    r'NO\ WAI'
    return t


def t_IF_END(t):
    r'OIC'
    return t


def t_PLUS(t):
    r'SUM\ OF'
    return t


def t_MINUS(t):
    r'DIFF\ OF'
    return t


def t_MULTIPLY(t):
    r'PRODUKT\ OF'
    return t


def t_DIVIDE(t):
    r'QUOSHUNT\ OF'
    return t


def t_MOD(t):
    r'MOD\ OF'
    return t


def t_MAX(t):
    r'BIGGR\ OF'
    return t


def t_MIN(t):
    r'SMALLR\ OF'
    return t


def t_EQUALS(t):
    r'\bR\b'
    return t


def t_PRINT(t):
    r'VISIBLE'
    return t


def t_INPUT(t):
    r'GIMMEH'
    return t


def t_VAR(t):
    r'I\ HAS\ A'
    return t


def t_ITZ(t):
    r'ITZ'
    return t


def t_AN(t):
    r'\bAN\b'
    t.type = 'AN'
    return t


def t_YARN(t):
    r'\"[^"]*\"'
    # t.type = "YARN"
    t.value = str(t.value[1:-1])
    return t


def t_NUMBAR(t):
    r'[+-]?[0-9]+[.][0-9]*'
    # t.type = "NUMBAR"
    t.value = float(t.value)
    return t


def t_NUMBR(t):
    r'\d+'
    # t.type = "NUMBR"
    t.value = int(t.value)
    return t


def t_TROOF(t):
    r'WIN|FAIL'
    # t.type = "TROOF"
    if t.value == "WIN":
        t.value = True
    else:
        t.value = False
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += 1
    return t


def t_comment(t):
    r"[ ]*BTW[^\n]*"
    pass


def t_TYPE(t):
    r'NUMBR|NUMBAR|YARN|TROOF'
    return t


def t_CHANGE_TYPE(t):
    r'IS\ NOW\ A'
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = "NAME"
    # t.type = RESERVED.get(t.value, 'NAME')
    return t


def t_error(t):
    print("Illegal characters! {s}".format(s=t))
    t.lexer.skip(1)


t_ignore = ' \t\n'

lexer = lex.lex()

precedence = (
    ('left', "PLUS", "MINUS"),
    ("left", "EQUALS"),
    ('left', "IF_END"),
    ("left", "NAME", "VAR"),
)


def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    out = run(p[1])

    if out:
        print(out)


def p_expression_logic(p):
    '''
    expression : LOGIC_EQUALS expression AN expression
            | LOGIC_DIFFER expression AN expression
            | LOGIC_AND expression AN expression
            | LOGIC_OR expression AN expression
            | LOGIC_XOR expression AN expression
    '''
    p[0] = (p[1], p[2], p[4])


def p_expression_logic_not(p):
    '''
    expression : LOGIC_NOT expression
    '''
    p[0] = ("not", p[2])


def p_expression_logic_multi(p):
    '''
    expression : LOGIC_ALL expression LOGIC_END
                | LOGIC_ALL expression AN expression LOGIC_END
                | LOGIC_ALL expression AN expression AN expression LOGIC_END
                | LOGIC_ALL expression AN expression AN expression AN expression LOGIC_END
                | LOGIC_ANY expression LOGIC_END
                | LOGIC_ANY expression AN expression LOGIC_END
                | LOGIC_ANY expression AN expression AN expression LOGIC_END
                | LOGIC_ANY expression AN expression AN expression AN expression LOGIC_END

    '''
    p[0] = (p[1], p[2::2])


def p_expression_EQUALS(p):
    '''
    empty : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])


def p_var_assign(p):
    '''
    var_assign : VAR NAME ITZ expression
    '''
    p[0] = ('init', p[2], p[4])


def p_ver_assign_empty(p):
    '''
    var_assign : VAR NAME
    '''
    p[0] = ("init_empty", p[2])


def p_expression_TYPE(p):
    '''
    expression : NUMBR
                | NUMBAR
                | YARN
                | TROOF
    '''
    p[0] = p[1]


class IF:
    expression = None
    if_yes = None
    if_no = None


if_list = list()


def p_parse_if_start(p):
    '''
    empty : expression IF_START
    '''
    if_ = IF()
    if_.expression = p[1]
    if_list.append(if_)


def p_parse_if_yes(p):
    '''
    empty : IF_YES expression
    '''
    if_list[-1].if_yes = p[2]


def p_parse_if_no(p):
    '''
    empty : IF_NO expression
    '''
    if_list[-1].if_no = p[2]


def p_parse_if_end(p):
    '''
    expression : IF_END
    '''
    if_ = if_list.pop()
    p[0] = ("if", if_.expression, if_.if_yes, if_.if_no)


def p_expression_print(p):
    '''
    expression : PRINT expression
    '''
    p[0] = ('print', p[2])


def p_expression_input(p):
    '''
    expression : INPUT NAME
    '''
    p[0] = ("input", p[2])


def p_expression(p):
    '''
    expression : PLUS expression AN expression
                | MINUS expression AN expression
                | MULTIPLY expression AN expression
                | DIVIDE expression AN expression
                | MOD expression AN expression
                | MAX expression AN expression
                | MIN expression AN expression
    '''
    p[0] = ("OP", p[1], p[2], p[4])


def p_expression_type_change(p):
    '''
    empty : NAME CHANGE_TYPE TYPE
    '''
    p[0] = ('cast', p[1], p[3])


def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])


def p_error(p):
    print("Syntax error with {a}".format(a=str(p)))


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


def lex_check(st):
    lexer.input(st)

    while True:
        tok = lexer.token()
        if not tok:
            break
        print("TOKEN: " + str(tok))


parser = yacc.yacc()
variables = {}


def run(p):
    # print(p) #DEBUG
    if type(p) == tuple:
        if p[0] == "OP":
            v1 = run(p[2])
            v2 = run(p[3])
            operation = p[1]
            if operation == "SUM OF":
                return v1 + v2
            elif operation == "DIFF OF":
                return v1 - v2
            elif operation == "PRODUKT OF":
                return v1 * v2
            elif operation == "QUOSHUNT OF":
                return v1 / v2
            elif operation == "MOD OF":
                return v1 % v2
            elif operation == "BIGGR OF":
                return max(v1, v2)
            elif operation == "SMALLR OF":
                return min(v1, v2)

        if p[0] == "init":
            variables[p[1]] = run(p[2])
        if p[0] == "init_empty":
            variables[p[1]] = None
        if p[0] == "=":
            if p[1] not in variables:
                raise Exception("Undeclared variable found! {v}".format(v=p[1]))
            else:
                variables[p[1]] = run(p[2])
            return

        if p[0] == 'var':
            if p[1] not in variables:
                raise Exception("Undeclared variable found! {v}".format(v=p[1]))
            else:
                return variables[p[1]]
        if p[0] == "print":
            # print("vis with p = {q}".format(q=p))
            # print(variables)
            print(run(p[1]))
            return
        if p[0] == "cast":
            if p[1] not in variables:
                raise Exception("Undeclared variable found! {v}".format(v=p[1]))
            v = variables[p[1]]
            if p[2] == "NUMBR":
                v = int(v)
            elif p[2] == "NUMBAR":
                v = float(v)
            elif p[2] == "TROOF":
                v = bool(v)
            else:
                v = str(v)
            variables[p[1]] = v
            return
        if p[0] == "BOTH SAEM":
            return run(p[1]) == run(p[2])
        if p[0] == "DIFFRINT":
            return run(p[1]) != run(p[2])

        if p[0] == "if":
            if run(p[1]):
                return run(p[2])
            else:
                return run(p[3])

        if p[0] == "BOTH OF":
            b1 = run(p[1])
            b2 = run(p[2])
            return b1 and b2
        if p[0] == "EITHER OF":
            b1 = run(p[1])
            b2 = run(p[2])
            return b1 or b2
        if p[0] == "WON OF":
            b1 = run(p[1])
            b2 = run(p[2])
            return b1 != b2
        if p[0] == "NOT":
            b = run(p[1])
            return not b
        if p[0] == "ALL OF":
            for b in p[1]:
                if not run(b):
                    return False
            return True
        if p[0] == "ANY OF":
            for b in p[1]:
                if run(b):
                    return True
            return False
        if p[0] == 'input':
            variables[p[1]] = raw_input(">>> ")
            return

    else:
        return p


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Process some LolCode.')
    arg_parser.add_argument('-f', nargs=1, help='input filename')
    args = arg_parser.parse_args()
    filename = args.f[0]
    with open(filename, 'r') as f:
        for line in f:
            # lex_check(line)
            if line:
                try:
                    parser.parse(line)
                except Exception as e:
                    print(line)
                    lex_check(line)
                    raise e
