import ply.yacc as yacc

from lex import tokens
import AST

vars = {}

def p_executable(p):
    ''' executable : function newline '''
    p[0] = AST.ExecutableNode(p[1])

def p_executable_recursive(p):
    ''' executable : function newline executable '''
    p[0] = AST.ExecutableNode([p[1]]+p[3].children)

def p_programme_statement(p):
    ''' programme : statement newline'''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement newline programme '''
    p[0] = AST.ProgramNode([p[1]]+p[3].children)

def p_function_noargs(p):
    ''' function : FONCTION IDENTIFIER '(' ')' newline DEBUT newline programme FINFONCTION'''
    p[0] = AST.FunctionNode([p[2], 0, p[8]])

def p_function(p):
    ''' function : FONCTION IDENTIFIER '(' arguments ')' newline DEBUT newline programme FINFONCTION'''
    p[0] = AST.FunctionNode([p[2], p[4], p[9]])

def p_arguments(p):
    ''' arguments : IDENTIFIER '''
    p[0] = [p[1]]

def p_arguments_recursive(p):
    ''' arguments : IDENTIFIER ',' arguments '''
    p[0] = [p[1]]+p[3]

def p_arguments_val(p):
    ''' argval : expression '''
    p[0] = [p[1]]

def p_arguments_val_recurse(p):
    ''' argval : expression ',' argval '''
    p[0] = [p[1]] + p[3]

def p_statement(p):
    ''' statement : assignation
        | structure '''
    p[0] = p[1]

def p_statement_print(p):
    ''' statement : AFFICHE expression '''
    p[0] = AST.PrintNode(p[2])

def p_statement_call(p):
    ''' statement : APPELLE IDENTIFIER '(' argval ')' '''
    p[0] = AST.CallNode([p[2], p[4]])

def p_structure(p):
    ''' structure : TANT QUE expression FAIRE newline programme FINTANTQUE '''
    p[0] = AST.WhileNode([p[3],p[6]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])

def p_assign(p):
    ''' assignation : IDENTIFIER '=' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]),p[3]])

def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)

def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    if result:
        print (result)

        import os
        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0]+'-ast.pdf'
        graph.write_pdf(name)
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
