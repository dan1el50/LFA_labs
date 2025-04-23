from tokens import TokenType, Token
import re


class Lexer:
    TOKEN_PATTERNS = [
        (TokenType.FLOAT, r'\b\d+\.\d+\b'),  # Match floating-point numbers
        (TokenType.INT, r'\b\d+\b'),  # Match integers
        (TokenType.PLUS, r'\+'),
        (TokenType.MINUS, r'-'),
        (TokenType.MULTIPLY, r'\*'),
        (TokenType.DIVIDE, r'/'),
        (TokenType.POWER, r'\^'),
        (TokenType.LEFT_PAREN, r'\('),
        (TokenType.RIGHT_PAREN, r'\)'),
        (TokenType.SIN, r'\b(sin)\b'),
        (TokenType.COS, r'\b(cos)\b'),
        (TokenType.TG, r'\b(tg)\b'),
        (TokenType.CTG, r'\b(ctg)\b'),
        (TokenType.SPACE, r'\s+'),  # Include spaces in output
    ]
    def __init__(self, input_text):
        self.input_text = input_text
        self.tokens = []

    def tokenize(self):
        text = self.input_text
        while text:
            matched = False
            for token_type, pattern in self.TOKEN_PATTERNS:
                match = re.match(pattern, text)
                if match:
                    lexeme = match.group(0)
                    self.tokens.append(Token(token_type, lexeme))  # Include SPACE tokens
                    text = text[len(lexeme):]  # Move forward in the string
                    matched = True
                    break

            if not matched:
                # Handle unknown characters
                self.tokens.append(Token(TokenType.UNKNOWN, text[0]))
                text = text[1:]

        return self.tokens