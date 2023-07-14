from typer import Typer
from scanner import Scanner, UnknownTokenError
from tabulate import tabulate

app = Typer()


@app.command()
def compile(file_address):
    rules = [
        ('IF_KW',          r'if'),
        ('ELSE_KW',        r'else'),
        ('FOR_KW',         r'for'),
        ('CONST_STR',      r'".*?"|\'.*?\''),
        ('CONST_NUMBER',   r'\d+'),
        ('while_KW', r'while'),
        ('switch_KW', r'switch'),
        ('using_KW', r'using'),
        ('return_KW', r'return'),
        ('namespace_KW', r'namespace'),
        ('case_KW', r'case'),
        # ('Function_KW', r'function'),
        ('int_KW', r'int'),
        ('float_KW', r'float'),
        ('Null_KW', r'Null'),
        # ('cin_KW' , r'cin'),
        # ('cout_KW' , r'cout'),

        ('comment', r'\/\*[\s,\S]*?\*\/'),
        ('cpp_comment',r'\/\/.*'),

        ('PLUS_OP',        r'\+'),
        ('increment_OP',     r'\++'),
        ('Reduce_OP',     r'\--'),
        ('MINUS_OP',       r'\-'),
        ('MULTIPLY_OP',    r'\*'),
        ('DIVIDE_OP',      r'\/'),
        ('LP',             r'\('),
        ('LCB',            r'\{'),
        ('RP',             r'\)'),
        ('RCB',            r'\}'),
        ('EQUAL_OP',       r'=='),
        ('ASSIGNMENT_OP',  r'='),
        ('OP_NOT_EQUALS', r'!='),
        ('GRATER', r'>'),
        ('LOWER', r'<'),
        ('grater_equal_OP', r'>='),
        ('lower_equal_OP', r'<='),

        ('OP_MOD', r'\%'),
        ('or_logop', r'\|\|'),
        ('and_logop', r'&&'),

        
        ('SEMICOLON',      r';'),
        ('COMMA', r','),
        ('COLON', r':'),
        ('L_BRACE', r'{'),
        ('R_BRACE', r'}'),
        ('L_BRACKET',r'\['),
        ('R_BRACKET', r'\]'),

        ('IDENTIFIER',     r'[a-zA-Z_]\w*'),
        ('PREPROCESSOR_DIRECTIVES',     r'#[a-zA-Z].*')
    ]

    scanner = Scanner(rules, open(file_address, 'r').read())
    try:
        headers = ['Line', 'Column', 'Value', 'Type']
        tayble = [str(token).split('\t') for token in scanner.token_generator()]
        
        print(tabulate(tayble,headers,tablefmt="fancy_grid",stralign="center",disable_numparse=True))
        
    except UnknownTokenError as error:
        print(error)


if __name__ == '__main__':
    app()
