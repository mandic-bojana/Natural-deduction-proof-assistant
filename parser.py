#!/usr/bin/env python

from formulas import *
import ply.lex
import ply.yacc


def parse(text):

    keywords = {'exists': 'EXISTS', 'forall': 'FORALL',
                'true': 'TRUE', 'false': 'FALSE'}

    tokens = (['VARIABLE', 'PREDICATE_SYMBOL', 'COLON', 'COMMA', 'LPAREN', 'RPAREN',
               'EQ', 'NOT', 'AND', 'OR', 'IMPLIES'] +
              list(keywords.values()))

    def t_VARIABLE(t):

        r'[A-Z][A-Za-z0-9_]*'
        t.type = keywords.get(t.value,'VARIABLE')
        t.value = Variable(t.value)
        return t


    def t_PREDICATE_SYMBOL(t):

        r'[a-z][a-z0-9]*'
        t.type = keywords.get(t.value,'PREDICATE_SYMBOL')
        return t


    t_EQ = r'<=>'
    t_NOT = r'~'
    t_AND = r'/\\'
    t_OR = r'\\/'
    t_IMPLIES = r'->'
    t_COLON = r':'
    t_COMMA = r','
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    t_ignore = ' \t\n'

    def t_newline(t):

        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(t):

        line = t.value.lstrip()
        i = line.find('\n')
        line = line if i == -1 else line[:i]
        raise ValueError('Syntax error, line {0}: {1}'
                         .format(t.lineno + 1, line))
    
    def p_formula_quantifier(p):

        '''formula : FORALL VARIABLE COLON formula
                   | EXISTS VARIABLE COLON formula'''
        p[0] = Forall(p[2], p[4]) if p[1] == 'forall' else Exists(p[2], p[4])
 
    def p_formula_binary(p):

        '''formula : formula EQ formula
                   | formula IMPLIES formula
                   | formula OR formula
                   | formula AND formula'''
        
        if p[2] == '<=>':
            p[0] = Equivalention(p[1], p[3])

        elif p[2] == '->':
            p[0] = Implication(p[1], p[3])

        elif p[2] == '\\/':
            p[0] = Disjunction(p[1], p[3])

        else:
            p[0] = Conjunction(p[1], p[3])


    def p_formula_not(p):

        'formula : NOT formula'
        p[0] = Not(p[2])

    def p_formula_boolean(p):

        '''formula : FALSE
                   | TRUE'''
        p[0] = TrueClass() if p[1] == 'true' else FalseClass()


    def p_formula_group(p):

        'formula : LPAREN formula RPAREN'
        p[0] = p[2]


    def p_formula_predicate(p):

        'formula : predicate'
        p[0] = p[1]


    def p_predicate(p):

        '''predicate : PREDICATE_SYMBOL LPAREN arg_list RPAREN
                | PREDICATE_SYMBOL'''
        p[0] = Predicate(p[1], []) if len(p) == 2 else Predicate(p[1], p[3])


    def p_arg_list(p):

        '''arg_list : term COMMA arg_list
                    | term'''
        p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[3]


    def p_term(p):

        '''term : PREDICATE_SYMBOL LPAREN arg_list RPAREN
                | VARIABLE'''
        p[0] = p[1] if len(p) == 2 else FunctionTerm(p[1], p[3])
        

       
    def p_error(p):

        if p is None:
            raise ValueError('Unknown error')

        raise ValueError('Syntax error, line {0}: {1}'.format(
                         p.lineno + 1, p.type))

# from lowest to highest precedence
    precedence = (('left', 'FORALL', 'EXISTS'),
                  ('left', 'COLON'),
                  ('left', 'EQ'),
                  ('left', 'IMPLIES'),
                  ('left', 'OR'),
                  ('left', 'AND'),
                  ('right', 'NOT'))

    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    try:
        return parser.parse(text, lexer=lexer)
    except ValueError as err:
        print(err)
        return []
    

def main():
    
    a = raw_input('Input formula: ')
    print(parse(a))



