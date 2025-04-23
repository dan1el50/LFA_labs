# Laboratory work nr. 3 - Lexer & Scanner
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


## Objectives:
1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

Note: Just because too many students were showing me the same idea of lexer for a calculator, I've decided to specify requirements for such case. Try to make it at least a little more complex. Like, being able to pass integers and floats, also to be able to perform trigonometric operations (cos and sin). But it does not mean that you need to do the calculator, you can pick anything interesting you want

# Implementation description
## *1.Tokens*
### *Token Definition and Constructor*
```
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
```
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
```
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

## *3.Main*
```
from lexer import Lexer

expression = input("Enter an arithmetic expression: ")
lexer = Lexer(expression)
tokens = lexer.tokenize()
for token in tokens:
    print(token)

```
This block represents the main execution of the program, where the lexer is used to process user input. It first prompts the user to enter an arithmetic expression, which is then passed as an argument to create a `Lexer` object. The `tokenize` method is called to analyze the input and generate a list of tokens. Finally, each token in the list is printed to the console, displaying its type and corresponding lexeme.

## *Output*
![image](https://github.com/user-attachments/assets/5ef3f0c5-2eb8-44fa-9e66-33c503805544)

# Conclusion
In this laboratory work, I implemented a lexer that breaks down arithmetic expressions into structured tokens. The lexer successfully identifies integers, floating-point numbers, arithmetic operators, parentheses, and trigonometric functions. By using regular expressions, I was able to efficiently scan the input and categorize lexemes while also handling spaces and unrecognized characters.

One of the main challenges I faced was ensuring that floating-point numbers were correctly detected before integers to prevent misclassification. I solved this by prioritizing FLOAT tokens in the matching process. Additionally, I implemented a way to handle unknown characters, allowing the lexer to detect and report invalid input.

Through this implementation, I gained a deeper understanding of lexical analysis and how tokenization is used in compilers and interpreters. This lexer could be further improved by adding support for more mathematical functions or enhancing error handling. Overall, this project helped me better understand how text processing and tokenization play a crucial role in language parsing.

## References
- https://stackoverflow.com/questions/55571086/writing-a-lexer-for-a-new-programming-language-in-python
- https://medium.com/@pythonmembers.club/building-a-lexer-in-python-a-tutorial-3b6de161fe84
