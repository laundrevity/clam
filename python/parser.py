from lexer import lex

class Node:
    pass

class VarDeclaration(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class PrintStatement(Node):
    def __init__(self, expression):
        self.expression = expression

class BinaryOperation(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Identifier(Node):
    def __init__(self, name):
        self.name = name

class Integer(Node):
    def __init__(self, value):
        self.value = value

def parse(tokens):
    tokens = list(tokens) # ensure we can use next() and iter() on tokens
    statements = []

    while tokens:
        token_type, value = tokens.pop(0)

        if token_type == 'KEYWORD' and value == 'var':
            _, name = tokens.pop(0)
            _, _ = tokens.pop(0) # equals sign
            _, value = tokens.pop(0)
            node = VarDeclaration(name, Integer(value))
            statements.append(node)
        
        elif token_type == 'KEYWORD' and value == 'print':
            _, name = tokens.pop(0)
            if tokens[0][1] in ['+', '-', '*', '/']:
                _, operator = tokens.pop(0)
                _, right_value = tokens.pop(0)
                node = PrintStatement(BinaryOperation(Identifier(name), operator, Identifier(right_value)))
            else:
                node = PrintStatement(Identifier(name))
            statements.append(node)
    
    return statements
