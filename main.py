import ast

class NumberFinder(ast.NodeVisitor):
    def __init__(self):
        self.defined_functions=set()
        self.defined_variable=set()
        self.used_symbol=set()
    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.generic_visit(node)
    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target,ast.Tuple):
               for element in target.elts:
                   if isinstance(element,ast.Name):
                      self.defined_variable.add(element.id)
            elif isinstance(target,ast.Name):
                self.defined_variable.add(target.id)
        self.generic_visit(node)
    def visit_Call(self, node):
        if isinstance(node.func,ast.Name):
            self.used_symbol.add(node.func.id)
        self.generic_visit(node)
    def visit_Name(self, node):
        if isinstance(node.ctx,ast.Load):
            self.used_symbol.add(node.id)
        self.generic_visit(node)
    def report(self):

        dead_function=self.defined_functions-self.used_symbol
        dead_variable=self.defined_variable-self.used_symbol
        for func in dead_variable:
            print(f"The variable is declared but never used:{func}")
        for func in dead_function:
            print(f"The function is declared but never called:{func}")

class NumberChanger(ast.NodeTransformer):
    def visit_BinOp(self, node):
        if not isinstance(node.op, ast.Add):
            return self.generic_visit(node)
        first=None
        second=None
        if isinstance(node.left,ast.Constant) and isinstance(node.right,ast.Name):
                first=node.left
                second=node.right
        elif isinstance(node.right,ast.Constant) and isinstance(node.left, ast.Name):
                first=node.right
                second=node.left
        if first and second:
            print("Found a string concatenation to convert!")
            return ast.JoinedStr(values=[first,ast.FormattedValue(value=second,conversion=-1)])

        return node
    def visit_Call(self, node):
        if isinstance(node.func,ast.Attribute) and node.func.attr=="format":
            if isinstance(node.func.value,ast.Constant) and isinstance(node.func.value.value,str):
                print("Found a .format() call to convert")
                orignal_string=node.func.value.value
                sting_part=ast.Constant(value=orignal_string.replace("{}",""))
                var_part=node.args[0]
                formatted_value=ast.FormattedValue(value=var_part,conversion=-1)
                return ast.JoinedStr(values=[sting_part,formatted_value])
        return self.generic_visit(node)

    def visit_FunctionDef(self, node):
        string_arg= ast.Constant(value=f"Entering function {node.name}")
        string_func=ast.Name(id="print",ctx=ast.Load())
        string_call=ast.Call(func=string_func,args=[string_arg])
        print_exp_node=ast.Expr(value=string_call)
        node.body.insert(0,print_exp_node)
        self.generic_visit(node)
        return node





source_code = """
x,y,z=3
y=6
"Hello, " + name
"Hello, {}".format(name)
f"hello,{name}"
3+4
def fun(heh):
   x=1+2
   print("hello world")
   return x
z=y
fun(x)
"""
tree = ast.parse(source_code)
print(ast.dump(tree,indent=3))

detector = NumberFinder()
detector.visit(tree)
detector.report()


