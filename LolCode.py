from ply import yacc
from ply import lex

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

    "PLUS",
    "MINUS",
    "MULTIPLY",
    "DIVIDE",
    "EQUALS",
    "MOD",
    "MAX",
    "MIN",

    "CHANGE_TYPE",

    "PRINT",
    "INPUT"
]


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
    r'R'
    return t


def t_PRINT(t):
    r'VISIBLE'
    return t


def t_INPUT(t):
    r'GIMMEG'
    return t


def t_VAR(t):
    r'I\ HAS\ A'
    return t


def t_ITZ(t):
    r'ITZ'
    return t


def t_AN(t):
    r'AN'
    t.type = 'AN'
    return t


def t_YARN(t):
    r'\".*\"'
    t.type = "YARN"
    t.value = str(t.value[1:-1])
    return t


def t_NUMBAR(t):
    r'[+-]?[0-9]+[.][0-9]*'
    t.type = "NUMBAR"
    t.value = float(t.value)
    return t


def t_NUMBR(t):
    r'\d+'
    t.type = "NUMBR"
    t.value = int(t.value)
    return t


def t_TROOF(t):
    r'WIN|FAIL'
    t.type = "TROOF"
    t.value = True if t.value == "WIN" else False
    return t


def t_NEWLINE(t):
    r'\n'
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


t_ignore = r' '

lexer = lex.lex()

precedence = (
    ('left', "PLUS", "MINUS"),
    ("left", "EQUALS"),
    ("left", "NAME", "VAR")
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


def p_expression_NUMBR(p):
    '''
    expression : NUMBR
                | NUMBAR
                | YARN
    '''
    p[0] = p[1]


def p_expression_uno_operation(p):
    '''
    expression : PRINT expression
                | INPUT NAME
    '''
    p[0] = (p[1], p[2])


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


def p_experssion_var(p):
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
    if type(p) == tuple:
        if p[0] == "OP":
            v1_raw = p[2]
            if type(v1_raw) == tuple and v1_raw[0] == 'var':
                v1 = variables[v1_raw[1]]
            else:
                v1 = run(v1_raw)
            v2_raw = p[3]
            if type(v2_raw) == tuple and v2_raw[0] == 'var':
                v2 = variables[v2_raw[1]]
            else:
                v2 = run(v2_raw)
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

        if p[0] == "VISIBLE":
            # print("vis with p = {q}".format(q=p))
            # print(variables)
            if p[1][0] == "var":
                var_name = p[1][1]
                if var_name not in variables:
                    raise Exception("Undeclared variable found! {v}".format(v=var_name))
                else:
                    print(variables[var_name])
            else:
                print(run(p[1]))
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
        if p[0] == "GIMMEH":
            # doesn't work!
            variables[p[1]] = input()

    else:
        return p


prg = """
I HAS A VAR2
I HAS A VAR ITZ SUM OF 1 AN 2
VAR R BIGGR OF 50 AN 10
VISIBLE VAR
GIMMEG VAR2
BTW VAR2 R "WOW"
VISIBLE VAR2
"""

prg = """
VISIBLE PRODUKT OF 2 AN 2
VISIBLE "10"
"""

prg = """
I HAS A VAR
I HAS A VAR2
VAR R "10"
VAR IS NOW A NUMBR
VAR2 R PRODUKT OF VAR AN VAR
VISIBLE VAR
VISIBLE VAR2
"""

lex_check("VAR2 R PRODUKT OF VAR AN 2")
for line in prg.split("\n"):
    if line:
        try:
            parser.parse(line)
        except Exception as e:
            print(line)
            lex_check(line)
            raise e

# st1 = "I HAS A VAR ITZ SUM OF 1 AN 2"
# lex_check(st1)
# st2 = "VAR R BIGGR OF 50 AN 10"
# lex_check(st2)
# st3 = "VISIBLE VAR"
# lex_check(st3)

# parser.parse(st1)
# parser.parse(st2)
# parser.parse(st3)
