import ast

class NumberFinder(ast.NodeVisitor):
    def snake_case(self,string):
        for char in string:
            if char.isupper():
                return True
        return False

    def visit_FunctionDef(self, node):
        print(f"Found Function Definition:{node.name}")
        if self.snake_case(node.name):
            print(f"-> WARNING: Function '{node.name}' is not snake_case")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func,ast.Name):
            print(f"Found Function Call: {node.func.id}")
        elif isinstance(node.func,ast.Attribute):
            print(f"Found Function Call: {node.func.value.id}.{node.func.attr}")


code = """
def parent_function():
    def child_function():
        pass
"""
l=ast.parse(code)
print(ast.dump(l))
finder=NumberFinder()
finder.visit(l)

