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
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])

def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]]+p[2].children)

def p_condition(p):
    '''statement : SI expression ALORS newline programme FINSI'''
    p[0] = AST.CondNode([p[2], p[5]])

def p_condition_else(p):
    '''statement : SI expression ALORS newline programme SINON newline programme FINSI'''
    p[0] = AST.CondNode([p[2], p[5], p[8]])

def p_function_noargs(p):
    ''' function : FONCTION IDENTIFIER '(' ')' newline DEBUT newline programme FIN'''
    p[0] = AST.FunctionNode([AST.TokenNode(p[2]), AST.TokenNode(0), p[8]])

def p_function_noargs_return(p):
    ''' function : FONCTION IDENTIFIER '(' ')' newline DEBUT newline programme RETOURNE IDENTIFIER newline FIN'''
    p[0] = AST.FunctionNode([AST.TokenNode(p[2]), AST.TokenNode(0), p[8], AST.TokenNode(p[10])])

def p_function(p):
    ''' function : FONCTION IDENTIFIER '(' arguments ')' newline DEBUT newline programme FIN'''
    p[0] = AST.FunctionNode([AST.TokenNode(p[2]), AST.TokenNode(p[4]), p[9]])

def p_function_return(p):
    ''' function : FONCTION IDENTIFIER '(' arguments ')' newline DEBUT newline programme RETOURNE IDENTIFIER newline FIN'''
    p[0] = AST.FunctionNode([AST.TokenNode(p[2]), AST.TokenNode(p[4]), p[9], AST.TokenNode(p[11])])

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

def p_statement_newline(p):
    ''' statement : newline '''
    p[0] = AST.NewLineNode()

def p_statement_print(p):
    ''' statement : AFFICHE expression '''
    p[0] = AST.PrintNode(p[2])

def p_statement_call_noargs(p):
    ''' statement : APPELLE IDENTIFIER '(' ')' '''
    p[0] = AST.CallNode([AST.TokenNode(p[2]), AST.TokenNode([])])

def p_statement_call_noargs_return(p):
    ''' statement : APPELLE IDENTIFIER '(' ')' DONNE IDENTIFIER '''
    p[0] = AST.CallNode([AST.TokenNode(p[2]), AST.TokenNode([]), AST.TokenNode(p[6])])

def p_statement_call(p):
    ''' statement : APPELLE IDENTIFIER '(' argval ')' '''
    p[0] = AST.CallNode([AST.TokenNode(p[2]), AST.TokenNode(p[4])])

def p_statement_call_return(p):
    ''' statement : APPELLE IDENTIFIER '(' argval ')' DONNE IDENTIFIER '''
    p[0] = AST.CallNode([AST.TokenNode(p[2]), AST.TokenNode(p[4]), AST.TokenNode(p[7])])

def p_statement_inc(p):
    '''statement : INC expression'''
    p[0] = AST.IncDecNode([p[2], AST.TokenNode('+')])

def p_statement_dec(p):
    '''statement : DEC expression'''
    p[0] = AST.IncDecNode([p[2], AST.TokenNode('-')])

def p_statement_input(p):
    ''' statement : LIRE IDENTIFIER '''
    p[0] = AST.InputNode([AST.TokenNode(p[2])])

def p_statement_pyexec(p):
    ''' statement : NALEAT IDENTIFIER '''
    p[0] = AST.PyExecNode([AST.TokenNode(p[2])])

def p_structure(p):
    ''' structure : TANT QUE expression FAIRE newline programme FINTANTQUE '''
    p[0] = AST.WhileNode([p[3],p[6]])

def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression
            | expression CMP_OP expression
            | expression EQ_OP expression
            | expression NEQ_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])

def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])

def p_expression_string(p):
    '''expression : STRING '''
    p[0] = AST.TokenNode(AST.TokenNode(p[1]))

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

yacc.yacc(outputdir='generated', debug=0)

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
