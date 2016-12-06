import AST
from AST import addToClass
from functools import reduce

operations = {
    '+' : lambda x,y: x+y,
    '-' : lambda x,y: x-y,
    '*' : lambda x,y: x*y,
    '/' : lambda x,y: x/y,
}

_funcs = {}
_vars = {}

_running_function = None

@addToClass(AST.FunctionNode)
def execute(self):
    _funcs[self.children[0]] = {}
    _funcs[self.children[0]][0] = self.children[2]
    _funcs[self.children[0]][1] = {}
    if self.children[1] != 0:
        for arg in self.children[1]:
            _funcs[self.children[0]][1][arg] = None

@addToClass(AST.CallNode)
def execute(self):
    global _running_function
    _running_function = self.children[0]

    i = 0
    keys = []
    for k in _funcs[_running_function][1].keys():
        keys.append(k)
    for k in keys:
        _funcs[_running_function][1][k] = self.children[1][i].tok
        i += 1
    _funcs[_running_function][0].execute()
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
    return reduce(operations[self.op], args)

@addToClass(AST.AssignNode)
def execute(self):
    global _running_function
    _funcs[_running_function][1][self.children[0].tok] = self.children[1].execute()

@addToClass(AST.PrintNode)
def execute(self):
    print(self.children[0].execute())

@addToClass(AST.WhileNode)
def execute(self):
    while self.children[0].execute() != 0:
        self.children[1].execute()


if __name__ == "__main__":
    from parser import parse
    import sys
    prog = open(sys.argv[1]).read()
    ast = parse(prog)

    ast.execute()
    _running_function = "main"
    _funcs['main'][0].execute()
