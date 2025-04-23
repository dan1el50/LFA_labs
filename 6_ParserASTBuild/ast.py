class ASTNode:
    pass


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"Number({self.value})"


class UnaryOpNode(ASTNode):
    def __init__(self, operator, operand):
        self.operator = operator  # sin, cos, etc.
        self.operand = operand

    def __repr__(self):
        return f"{self.operator}({self.operand})"


class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator  # +, -, *, /, ^
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"
