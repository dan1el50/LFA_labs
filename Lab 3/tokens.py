from enum import Enum

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


# Step 2: Define Token Class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type.value} : '{self.value}'"