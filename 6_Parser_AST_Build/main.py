from lexer import Lexer
from parser import Parser
from ast_printer import print_ast  # <-- Import the pretty printer

def main():
    expression = input("Enter an arithmetic expression: ")
    lexer = Lexer(expression)
    tokens = lexer.tokenize()

    print("Tokens:")
    for token in tokens:
        print(token)

    # Remove space tokens before parsing
    tokens = [t for t in tokens if t.type.name != "SPACE"]

    parser = Parser(tokens)
    try:
        ast = parser.parse()
        print("\nAST Tree:")
        print_ast(ast)  # <-- Pretty print the tree
    except Exception as e:
        print(f"Parser error: {e}")

if __name__ == "__main__":
    main()
