import AST
from AST import addToClass
from functools import reduce

operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
    '<' : lambda x,y: 0 if x<y else 1,
    '>' : lambda x,y: 0 if x>y else 1,
    '==' : lambda x,y: 0 if x==y else 1,
    '!=' : lambda x,y: 0 if x!=y else 1
}

_funcs = {}
_vars = {}

_running_function = None

@addToClass(AST.PyExecNode)
def execute(self):
    from random import randrange
    global _running_function
    _funcs[_running_function][1][self.children[0].tok] = randrange(10000)


@addToClass(AST.FunctionNode)
def execute(self):
    from collections import OrderedDict
    funcName = self.children[0].tok
    _funcs[funcName] = {}
    _funcs[funcName][0] = self.children[2]
    _funcs[funcName][1] = OrderedDict()
    _funcs[funcName][3] = []
    if self.children[1].tok != 0:
        for arg in self.children[1].tok:
            _funcs[funcName][1][arg] = None
            _funcs[funcName][3].append(arg)
    if len(self.children) > 3:
        _funcs[funcName][2] = self.children[3]

@addToClass(AST.CallNode)
def execute(self):
    from collections import OrderedDict
    global _running_function
    next_function = str(self.children[0]).replace("'", "").rstrip()
    _funcs[next_function][1] = OrderedDict()
    for arg in _funcs[next_function][3]:
        _funcs[next_function][1][arg] = None
    i = 0
    keys = []
    for k in _funcs[next_function][1].keys():
        keys.append(k)
    for k in keys:
        _funcs[next_function][1][k] = self.children[1].tok[i].execute()
        i += 1
    _running_function = next_function
    _funcs[_running_function][0].execute()
    if len(self.children) > 2:
        return_val = str(_funcs[_running_function][2]).replace("'", "").rstrip()
        val = str(self.children[2]).replace("'", "").rstrip()
        _funcs["main"][1][val] = _funcs[_running_function][1][return_val]
    _running_function = "main"

@addToClass(AST.ExecutableNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.ProgramNode)
def execute(self):
    for c in self.children:
        c.execute()

@addToClass(AST.TokenNode)
def execute(self):
    global _running_function
    if isinstance(self.tok, AST.TokenNode):
        if isinstance(self.tok.tok, str):
            if self.tok.tok[0] == '"':
                return self.tok.tok[1:-1]
    if isinstance(self.tok, str):
        try:
            return _funcs[_running_function][1][self.tok]
        except KeyError:
            print("*** Error: Variable %s undefined !" % self.tok)
    return self.tok

@addToClass(AST.OpNode)
def execute(self):
    args = [c.execute() for c in self.children]
    if len(args) == 1:
        args.insert(0,0)
    if(isinstance(args[0], str)):
        for i in range(1, len(args)):
            args[i] = str(args[i])
    try:
        args = [c.tok if isinstance(c, AST.TokenNode) else c for c in args ]
        return reduce(operations[self.op], args)
    except TypeError:
        for arg in args:
            try:
                float(arg)
            except ValueError:
                print("Error:",arg,"is not a number !")
                exit(1)


@addToClass(AST.AssignNode)
def execute(self):
    global _running_function
    _funcs[_running_function][1][self.children[0].tok] = self.children[1].execute()

@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())

@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute() == 0:
        self.children[1].execute()

@addToClass(AST.IncDecNode)
def execute(self):
    global _running_function
    _funcs[_running_function][1][self.children[0].tok] = reduce(operations[self.children[1].tok], [self.children[0].execute(),1])

@addToClass(AST.CondNode)
def execute(self):
    cond_result = self.children[0].execute()
    if len(self.children) == 2:
        if cond_result != 0:
            self.children[1].execute()
    else:
        if cond_result == 0:
            self.children[1].execute()
        else:
            self.children[2].execute()

@addToClass(AST.InputNode)
def execute(self):
    global _running_function
    minput = input()
    _funcs[_running_function][1][self.children[0].tok] = int(minput) if minput.isdigit() or minput[1:].isdigit() else minput



if __name__ == "__main__":
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.execute()
    _running_function = "main"
    _funcs['main'][0].execute()
