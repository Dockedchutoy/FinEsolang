"""
Fin Esoteric Programming Language Prototype Interpreter

a prototype to experiment with the first version of the idea.

i'll probably just reuse a model i am pretty familiar with already so this really is just a test.
"""

import sys

# Initialization

# Token Object

class Tkn():
    def __init__(self, value, type) -> None:
        """
        Token object used by the interpreter

        The object support the following types:
        keyword* -- Various keywords representing statements (currently print;)
        string -- String type
        lineref -- Line Reference, stored as an integer (A negative value returns an error)
        offset -- Line offset, +x is to look x lines after, -x means look x lines before. (Going too high/low results in a error)
        nop -- Empty instruction.
        """
        self.value = value
        self.type = type
    
    def __repr__(self) -> str:
        return f"Tkn('{self.value}', '{self.type}')"

# Parser

class Parser():
    def __init__(self) -> None:
        pass

    def parse(self, source: str) -> list:
        lines = []
        tokens = []
        line = 0
        cur = 0
        token = ""

        keywords = ["print"]
        empty = [" ", "\t"]

        while cur < len(source):
            print(cur, source[cur])
            if source[cur].isalpha():   # Keywords
                while source[cur].isalpha():
                    token += source[cur]
                    cur += 1
                if token in keywords:
                    tokens.append(Tkn(token, token))
                
            elif source[cur] == "+" or source[cur] == "-":    # Line Offset
                token += source[cur]
                cur += 1
                while source[cur].isnumeric():
                    token += source[cur]
                    cur += 1
                tokens.append(Tkn(token, "offset"))
            
            elif source[cur] == '"':    # String
                cur += 1
                while not source[cur] == '"':
                    token += source[cur]
                    cur += 1
                cur += 1
                tokens.append(Tkn(token, "string"))
            
            elif source[cur] in empty:  # Empty chars
                while source[cur] in empty:
                    token += source[cur]
                    cur += 1
                tokens.append(Tkn(token, "nop"))

                
            elif source[cur] == "\n":   # Newline
                lines.append(tokens)
                tokens = []
                cur += 1
            
            else:
                cur += 1
            
            token = ""

        lines.append(tokens)

        return lines

# Interpreter

class Interpreter():
    def __init__(self) -> None:
        self.line = 0
        self.token = 0
        self.lines = []

    def exec_print(self) -> None:
        while self.lines[self.line][self.token].type == "nop":
            self.token += 1


    def interpret(self, lines) -> None:
        self.line = 0
        self.token = 0
        self.lines = lines

        while self.line < len(self.lines):

            while self.token < len(self.lines[self.line]):

                if self.lines[self.line][self.token].type == "print":
                    self.exec_print()

                self.token += 1

            self.line += 1
            self.token = 0

# Main Function

def main() -> None:
    code = 'print +1\n"Hello World!"'

    parser = Parser()
    lines = parser.parse(code)
    print(lines)

    interpreter = Interpreter()
    interpreter.interpret(lines)

    return

if __name__ == "__main__":
    main()