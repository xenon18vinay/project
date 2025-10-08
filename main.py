import ast
import argparse
class Symbol:
    def __init__(self,name,line):
        self.name=name
        self.line_number=line
        self.is_defined=True
        self.is_used=False
    def used(self):
        self.is_used=True
    def __repr__(self):
        return f"<Symbol(name'{self.name}',used={self.is_used})>"

class Scope:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.symbol = {}
        self.parent = parent
        self.children = []

class SymbolTableBuilder(ast.NodeVisitor):
    def __init__(self):
        # Generation of global scope
        self.root_scope=Scope(name="Global",parent=None)
        self.current_scope=self.root_scope

    def add_func_scope(self,name):
        #Function for adding new scope for first time using scope class
        new_node=Scope(name=name,parent=self.current_scope)
        self.current_scope.children.append(new_node)
        self.current_scope=new_node

    def visit_Import(self, node):
        for element in node.names:
            self.current_scope.symbol[element.name]=Symbol(element.name, node.lineno)
    def visit_FunctionDef(self, node):
        # This function Adds Func define in symbol table and changes scopes
        self.current_scope.symbol[node.name]=Symbol(node.name,node.lineno)
        self.add_func_scope(node.name)
        if isinstance(node.args.args,list):
            for argument in node.args.args:
                self.current_scope.symbol[argument.arg]=Symbol(argument.arg, argument.lineno)

        self.generic_visit(node)
        # updates the scope we are in
        self.current_scope=self.current_scope.parent

    def visit_Call(self, node):
        # This flips the is_used to true for called function
        if isinstance(node.func,ast.Name):
            temp_node=self.current_scope
            while temp_node:
                if node.func.id in temp_node.symbol:
                   temp_node.symbol[node.func.id].used()
                   break
                else:
                   temp_node=temp_node.parent

            # Need to add the LEGB- knowledge of built in functions for this warning
            # if not temp_node:
            #     print(f"Function {node.func.id} is not defined")
        self.generic_visit(node)


    def visit_Assign(self, node):
        # Adds variables to symbol table
        for target in node.targets:
            if isinstance(target,ast.Tuple):
               for element in target.elts:
                   if isinstance(element,ast.Name):
                      self.current_scope.symbol[element.id]=Symbol(element.id,element.lineno)
            elif isinstance(target,ast.Name):
                self.current_scope.symbol[target.id] = Symbol(target.id,target.lineno)
        self.generic_visit(node)

    def visit_Name(self, node):

        if isinstance(node.ctx,ast.Load):
            temp_node = self.current_scope
            while temp_node:
               if node.id in temp_node.symbol:
                  temp_node.symbol[node.id].used()
                  break
               else:
                   temp_node=temp_node.parent
            if not temp_node:
                print(f"The variable {node.id} is not defined")
        self.generic_visit(node)

    def report(self):
        print("--- Dead Code Report ---")
        self.recursive_report(self.root_scope)
        print("--- End of Report ---")

    def recursive_report(self,temp_scope):
        for key in temp_scope.symbol:
            if not temp_scope.symbol[key].is_used:
                print(f"In scope {temp_scope.name}: Unused symbol {key}-->(defined on {temp_scope.symbol[key].line_number}) ")
        for child in temp_scope.children:
            self.recursive_report(child)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Input a file path to the python tool.py by ( python tool.py [path_to_file]) for the dead code analysis")

    parser.add_argument("filepath",help="Input a file path by using command (python tool.py [path_to_file])")
    args = parser.parse_args()
    if not args.filepath.endswith(".py"):
        print(f"The file {args.filepath} is not a python file")
        exit()
    try:
       with open(args.filepath, "r") as file:
           file_code=file.read()
    except FileNotFoundError:
        print(f"ERROR: File not found at {args.filename}")
        exit()
    except Exception as e:
        print(f"ERROR:{e}")
        exit()

    tree = ast.parse(file_code)
    print(ast.dump(tree,indent=3))
    detector = SymbolTableBuilder()
    detector.visit(tree)
    detector.report()


