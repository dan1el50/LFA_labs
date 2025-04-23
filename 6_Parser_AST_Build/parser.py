from tokens import TokenType
from ast import NumberNode, UnaryOpNode, BinaryOpNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, token_type):
        token = self.current_token()
        if token and token.type == token_type:
            self.position += 1
            return token
        raise Exception(f"Expected token {token_type}, got {token}")

    def parse(self):
        result = self.expression()
        if self.current_token() is not None:
            raise Exception(f"Unexpected token: {self.current_token()}")
        return result

    def expression(self):
        node = self.term()
        while self.current_token() and self.current_token().type in (TokenType.PLUS, TokenType.MINUS):
            op_token = self.eat(self.current_token().type)
            right = self.term()
            node = BinaryOpNode(node, op_token.value, right)
        return node

    def term(self):
        node = self.factor()
        while self.current_token() and self.current_token().type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.eat(self.current_token().type)
            right = self.factor()
            node = BinaryOpNode(node, op_token.value, right)
        return node

    def factor(self):
        node = self.power()
        while self.current_token() and self.current_token().type == TokenType.POWER:
            op_token = self.eat(TokenType.POWER)
            right = self.power()
            node = BinaryOpNode(node, op_token.value, right)
        return node

    def power(self):
        token = self.current_token()
        if token and token.type in (TokenType.SIN, TokenType.COS, TokenType.TG, TokenType.CTG):
            func_token = self.eat(token.type)
            self.eat(TokenType.LEFT_PAREN)
            arg = self.expression()
            self.eat(TokenType.RIGHT_PAREN)
            return UnaryOpNode(func_token.value, arg)
        else:
            return self.atom()

    def atom(self):
        token = self.current_token()
        if token is None:
            raise Exception("Unexpected end of input")

        if token.type == TokenType.LEFT_PAREN:
            self.eat(TokenType.LEFT_PAREN)
            node = self.expression()
            self.eat(TokenType.RIGHT_PAREN)
            return node
        elif token.type in (TokenType.INT, TokenType.FLOAT):
            self.eat(token.type)
            return NumberNode(token.value)
        else:
            raise Exception(f"Unexpected token: {token}")
