from lexer import Lexer

expression = input("Enter an arithmetic expression: ")
lexer = Lexer(expression)
tokens = lexer.tokenize()
for token in tokens:
    print(token)
