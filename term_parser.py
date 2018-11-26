#!/usr/bin/env python

from formulas import *
import ply.lex
import ply.yacc


def parse_term(text):

    tokens = (['VARIABLE', 'FUNCTION_SYMBOL', 'COMMA', 'LPAREN', 'RPAREN'])

    def t_VARIABLE(t):

        r'[A-Z][A-Za-z0-9_]*'
        t.value = Variable(t.value)
        return t


    def t_FUNCTION_SYMBOL(t):

        r'[a-z][a-z0-9]*'
        return t


    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    t_ignore = ' \t\n'




    def p_term(p):
        '''term : FUNCTION_SYMBOL LPAREN arg_list RPAREN
                | VARIABLE'''
        p[0] = p[1] if len(p) == 2 else FunctionTerm(p[1], p[3])


    def p_arg_list(p):
        '''arg_list : term COMMA arg_list
                    | term'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]


    def p_error(p):
        if p is None:
            raise ValueError('Unknown error')
        raise ValueError('Syntax error, line {0}: {1}'.format(
                         p.lineno + 1, p.type))


    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(t):
        line = t.value.lstrip()
        i = line.find('\n')
        line = line if i == -1 else line[:i]
        raise ValueError('Syntax error, line {0}: {1}'
                         .format(t.lineno + 1, line))


    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()

    try:
        return parser.parse(text, lexer=lexer)

    except ValueError as err:
        print(err)
        return []


def main():
    
    text = raw_input('Input term: ')
    term = parse_term(text)
    print(term)

