# Laboratory work nr. 6 - Parser & Building an Abstract Syntax Tree
### Course: Formal Languages & Finite Automata
### Author: Cojocaru Daniel

----
# Theory

## *Lexer*
Lexical analysis is the first phase of a compiler and is responsible for breaking an input text (such as a source code file) into meaningful lexical tokens. This process is performed by a lexer (also called a scanner or tokenizer). The lexer reads a sequence of characters and groups them into lexemes, which are then categorized into tokens. For example this expression "3 + sin(45)" is passed to the lexer and it identifies the tokens and lesxemes like: INT -> '3'

## *Lexer vs. Tokens* 
There is an important distinction between lexemes and tokens:

Lexemes are the actual substrings extracted from the input (e.g., "3", "+", "sin").
Tokens are the categorized representation of lexemes, which do not necessarily retain the exact value of the lexeme but rather its type and potentially some metadata (e.g., `FLOAT`, `OPERATOR`, `FUNC`).

## *Purpose of the Lexer*
The main roles of a lexer include:

1. Recognizing valid tokens according to predefined rules.
2. Filtering out irrelevant elements such as non-defined characters or spaces if there is the case.
3. Generating structured data that can be used in later processing steps (such as syntax parsing in a compiler).
4. Detecting lexical errors by identifying invalid sequences of characters.

## *Tokenization Proccess*
Tokenization is the process of breaking down an input string into tokens using regular expressions or finite automata.

A finite state machine (FSM) is often used to implement a lexer, where:

- States represent progression in recognizing a token.
- Transitions occur based on character patterns.

For example:
1. Start in an initial state.
2. If the first character is a digit, move to a number state.
3. If a dot (.) follows, transition to a fractional part state.
4. If more digits follow, confirm as a valid FLOAT token.
5. If an invalid character appears, throw an error.

## *Parsing and Syntactic Analysis*
In the context of formal languages and compilers, parsing is the process of analyzing a string of symbols (usually tokens) to determine its grammatical structure with respect to a given formal grammar. Parsing transforms a linear sequence of tokens into a structured representation, typically a parse tree or an **abstract syntax tree (AST)**.

A parser is responsible for ensuring that the sequence of tokens follows the syntactic rules of the language. For example, it verifies whether an expression like `3 + 5 * 2` is valid and then organizes its structure according to operator precedence and associativity.

## *Abstract Syntax Tree (AST)*
An Abstract Syntax Tree (AST) is a hierarchical, tree-like structure that represents the abstract syntactic structure of source code. Unlike a parse tree, which retains all syntactic elements including punctuation and grouping, the AST omits unnecessary syntax details and focuses on the semantic essence of the input.

Each node in the AST denotes a construct occurring in the source code, such as:
- Literals like numbers
- Operators like `+`, `-`, `*`, `/`
- Function calls like `sin(x)` or `cos(3 + 2)`

This structure allows later stages of compilation or analysis (such as optimization or code generation) to work more effectively on a simplified representation.

## *Components Implemented in This Lab*
- Lexical Analyzer (Lexer): Transforms the input string into a list of tokens using regular expressions.
- Token Types: Each token is categorized using an enumerated TokenType, such as PLUS, FLOAT, or SIN.
- Recursive Descent Parser: A hand-written parser that uses recursive functions to follow grammar rules and build the AST.
- AST Node Definitions: Custom Python classes like NumberNode, BinaryOpNode, and UnaryOpNode are used to build the hierarchical representation.
- Tree Visualizer: A text-based printer displays the AST in a readable tree format using indentation.



## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
    1. In case you didn't have a type that denotes the possible types of tokens you need to:
        1. Have a type TokenType (like an enum) that can be used in the lexical analysis to categorize the tokens.
        2. Please use regular expressions to identify the type of the token.
    2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
    3. Implement a simple parser program that could extract the syntactic information from the input text.
  

# Implementation description
## *1.Tokens*
### *Token Definition and Constructor*
```python
class TokenType(Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    POWER = "POWER"
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    SIN = "SIN"
    COS = "COS"
    TG = "TG"
    CTG = "CTG"
    SPACE = "SPACE"
    UNKNOWN = "UNKNOWN"  # For error handling

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type.value} : '{self.value}'"
```
This code defines the TokenType enumeration and the `Token` class. The TokenType enum lists all possible token categories, including mathematical operators as well as trigonometric functions. It also includes token types for parentheses, numeric values like `INT` for integers and `FLOAT` for decimal numbers and a `SPACE` token which defines the simple space whereas the `UNKNOWN` type is used for handling unrecognized characters.

The Token class represents an individual token with two attributes: type, which holds the category of the token, and value, which stores the actual lexeme extracted from the input. The `__repr__ `method formats the token's output as a string, displaying its type and value. This block establishes the foundation of the lexer by defining how tokens are classified and represented during lexical analysis.

## *2.Lexer*
### *Regular expressions and constructor*
```python
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
```

This block defines the `Lexer` class, which is responsible for breaking an input string into tokens. The `TOKEN_PATTERNS` list contains predefined regular expressions for different token types. The order of these patterns is important, as floating-point numbers are matched before integers to prevent incorrect tokenization. Operators are matched using their respective symbols, while trigonometric functions are recognized as full words using word boundaries (`\b`). Parentheses are matched separately, and spaces are included to ensure they are recognized as tokens rather than ignored.

The `__init__` method initializes the lexer by storing the input string and creating an empty list to hold the extracted tokens. This class sets up the core mechanism for identifying different types of tokens from the input expression.

## *Tokenizer function*
```python
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
```
This block implements the `tokenize` method, which processes the input string and converts it into a list of tokens. The method iterates over the input text, attempting to match each portion of it against the predefined regular expressions in `TOKEN_PATTERNS`. If a match is found, the corresponding lexeme is extracted, converted into a Token object, and added to the tokens list. The matched portion of the text is then removed from the input, and the loop continues.

If no match is found for a character, it is classified as an `UNKNOWN` token, indicating an unrecognized or invalid input. The method ensures that every character in the input is processed, and at the end of execution, it returns the complete list of tokens. This function serves as the core logic of the lexer, systematically scanning and categorizing the input expression.

## *3.AST*
### *ATNode, NumberNode and UnaryOpNode classes*
```python
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
```
This block defines the structure of nodes used in the Abstract Syntax Tree (AST). The `ASTNode` class acts as a generic base class from which all specific node types inherit. The `NumberNode` class represents a numerical value, such as an integer or a float, and stores that value internally while also defining a method to print it in a human-readable format. The `UnaryOpNode` class is used to represent unary operations like mathematical functions (`sin`, `cos`, `tg`, `ctg`) and holds both the operator name and the operand, which itself is another AST node.

### *BinaryOpNode class*
```python
class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator  # +, -, *, /, ^
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"
```    
This class defines the structure of a binary operation node within the Abstract Syntax Tree. The `BinaryOpNode` inherits from the base `ASTNode` and is used to represent operations that involve two operands, such as addition, subtraction, multiplication, division, or exponentiation. It stores the left and right operands, both of which are AST nodes themselves, and the operator symbol between them. The `__repr__` method provides a string representation that visually reflects the operation in infix notation, making the AST easier to interpret when printed.

## *4.AST Printer*
```python
def print_ast(node, indent="", is_last=True):
    marker = "└── " if is_last else "├── "

    if hasattr(node, 'value') and not hasattr(node, 'left'):
        # NumberNode
        print(indent + marker + f"Number({node.value})")
    elif hasattr(node, 'operand'):
        # UnaryOpNode
        print(indent + marker + f"Function({node.operator})")
        print_ast(node.operand, indent + ("    " if is_last else "│   "), True)
    elif hasattr(node, 'left') and hasattr(node, 'right'):
        # BinaryOpNode
        print(indent + marker + f"Operation({node.operator})")
        print_ast(node.left, indent + ("    " if is_last else "│   "), False)
        print_ast(node.right, indent + ("    " if is_last else "│   "), True)
    else:
        # Fallback for unexpected nodes
        print(indent + marker + "UnknownNode")
```
This function is responsible for visually displaying the structure of an Abstract Syntax Tree in a readable, indented format in the terminal. It recursively traverses the tree, printing each node with a visual marker to indicate its position in the hierarchy. The function checks the type of node based on its attributes: if it contains a `value` and not a `left`, it is considered a `NumberNode`; if it has an `operand`, it is treated as a `UnaryOpNode`; and if it has both `left` and `right`, it is identified as a `BinaryOpNode`. For each case, the function prints the node's label with the appropriate indentation and continues recursively through its children. This produces a tree-like structure that makes it easy to understand the relationships between nodes.

## *5.Parser*
### *Initializer, current_token and eat functoins*
```python
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
```
This section defines the core structure of the `Parser` class, which is responsible for analyzing a list of tokens and building an Abstract Syntax Tree. When initialized, the parser stores the list of tokens and starts at the first position. The `current_token` method retrieves the token currently being examined, ensuring it does not exceed the list's bounds. The `eat` method is used to consume a token of a specific expected type; if the current token matches, the parser advances to the next one and returns it. If not, an exception is raised, signaling a syntax error. This mechanism is fundamental for moving through the input while verifying that the token sequence conforms to the grammar.

### *Parse, expression and term functions*
```python
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
```
This part of the parser defines how arithmetic expressions are interpreted. The `parse` method begins parsing from the highest-level rule and ensures no extra tokens remain. The `expression` method handles addition and subtraction by combining terms using `BinaryOpNode`. The `term` method handles multiplication and division similarly, ensuring correct operator precedence.

### *Factor and power functions*
```python
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
```
This part of the parser handles exponentiation and function calls. The `factor` method manages the right-associative `^` operator by combining expressions into `BinaryOpNode`s. The `power` method checks for functions like `sin`, `cos`, `tg`, or `ctg` followed by a parenthesized expression and wraps the result in a `UnaryOpNode`. If no function is found, it proceeds to parse a basic value using `atom()`.

### *Atom function*
```python
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
```
The `atom` method handles the most basic elements of an expression. It supports numbers by returning a `NumberNode` and allows grouped expressions by processing content inside parentheses. If an unexpected token is encountered or the input ends prematurely, it raises an error to indicate a syntax issue.

## *6.Main*
```
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
```
The `main` function serves as the entry point of the program. It takes an arithmetic expression as input, uses the lexer to tokenize it, and filters out space tokens. Then it initializes the parser with the cleaned token list and attempts to parse the expression into an AST. If successful, the AST is printed in a readable tree format; otherwise, any parsing errors are displayed.


## *Output*
![image](https://github.com/user-attachments/assets/338c0838-2b7c-4612-84ee-31908168825d)
![image](https://github.com/user-attachments/assets/490252cf-3775-4214-bad9-75dd0effd1df)

# Conclusion
This laboratory work deepened the understanding of parsing and the role of Abstract Syntax Trees (ASTs) in the analysis of programming language constructs. Starting from the output of a previously built lexical analyzer, we implemented a parser using the recursive descent method. This parser successfully interprets arithmetic expressions, including nested operations, functions like sin, cos, and mathematical operators with proper precedence and associativity.

The creation of specific AST node classes such as NumberNode, BinaryOpNode, and UnaryOpNode allowed us to construct a structured and simplified representation of the input text. This abstraction made it easier to follow the logical structure of expressions, omitting unnecessary syntactic details. Furthermore, we developed a text-based tree printer to visualize the AST directly in the terminal. This made the internal structure of expressions easier to interpret and debug.

By combining lexical analysis, syntactic analysis, and tree visualization, this lab successfully simulates an important part of how compilers and interpreters process source code. It also demonstrates how theoretical concepts like formal grammars and syntax rules are applied in practice through code. Overall, this work provided valuable insights into how raw text input can be turned into structured data, which is essential in the fields of compilers, interpreters, and formal language processing.

## References
- https://docs.python.org/3/library/argparse.html
- https://docs.python.org/3.9/library/parser.html
- https://docs.python.org/3/library/ast.html
