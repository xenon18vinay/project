import ast

class Scope:
    def __init__(self, name=None, parent=None):
        self.name = name
        self.symbol = {}
        self.parent = parent
        self.children = []

class SymbolTableBuilder(ast.NodeVisitor):
    def __init__(self):
        # Genration of global scope
        self.root_scope=Scope(name="Global",parent=None)
        self.current_scope=self.root_scope

    def add_func_scope(self,name):
        #adding new scope for first time using scope class
        new_node=Scope(name=name,parent=self.current_scope)
        self.current_scope.children.append(new_node)
        self.current_scope=new_node

    def visit_Import(self, node):
        for element in node.names:
            self.current_scope.symbol[element.name]={"name":f"{element.name}","is_defined":True,"is_used":False}
    def visit_FunctionDef(self, node):
        # This function Adds Func define in symbol table and changes scopes
        self.current_scope.symbol[node.name]={"name":f"{node.name}","is_defined":True,"is_used":False}
        self.add_func_scope(node.name)
        if isinstance(node.args.args,list):
            for argument in node.args.args:
                self.current_scope.symbol[argument.arg]={"name":f"{argument.arg}","is_defined":True,"is_used":False}

        self.generic_visit(node)
        # updates the scope we are in
        self.current_scope=self.current_scope.parent

    def visit_Call(self, node):
        # This flips the is_used to true for called function
        if isinstance(node.func,ast.Name):
            temp_node=self.current_scope
            while temp_node:
                if node.func.id in temp_node.symbol:
                   temp_node.symbol[node.func.id]["is_used"]=True
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
                      self.current_scope.symbol[element.id]={"name":f"{element.id}","is_defined":True,"is_used":False}
            elif isinstance(target,ast.Name):
                self.current_scope.symbol[target.id] = {"name": f"{target.id}", "is_defined": True, "is_used": False}
        self.generic_visit(node)

    def visit_Name(self, node):

        if isinstance(node.ctx,ast.Load):
            temp_node = self.current_scope
            while temp_node:
               if node.id in temp_node.symbol:
                  temp_node.symbol[node.id]["is_used"]=True
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
            if not temp_scope.symbol[key]["is_used"]:
                print(f"{temp_scope.name}:Unused--> {key}")
        for child in temp_scope.children:
            self.recursive_report(child)







source_code = """
import os  # Unused import

GLOBAL_DEAD = 'I am never used'
GLOBAL_USED = 'I am used'

def dead_function(): # Never called
    pass

def outer_function(arg_used, arg_dead): # 'arg_dead' is unused
    outer_var_used_by_inner = 100 # Used by the nested function
    outer_var_dead = 200          # Never used
    shadowed_var = 'outer value'  # Never used, as it is shadowed below

    def inner_function(inner_arg_dead): # 'inner_arg_dead' is unused
        # This variable shadows the one from the outer scope
        shadowed_var = 'inner value' # This is also an unused local variable
        
        # This uses a variable from the enclosing (outer) scope
        print(outer_var_used_by_inner)

    # This ensures 'inner_function' itself is not dead code
    inner_function('dead')
    # This ensures 'arg_used' is not dead code
    print(arg_used)

# --- Entry Point ---
def main():
    print(GLOBAL_USED)
    outer_function('used')

main()
"""
tree = ast.parse(source_code)
print(ast.dump(tree,indent=3))

detector = SymbolTableBuilder()
detector.visit(tree)
detector.report()


