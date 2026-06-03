"""
Second Fin Prototype Interpreter in Python
"""

import sys

# Error reporting

hadError = False
hadRuntimeError = False

def error(position, message):
    report(position, "", message)

def report(position, item, message):
    global hadError
    print(f"[{position}] Error{item}: {message}")
    hadError = True

def runtimeError(error):
    global hadRuntimeError
    print(f"[{error.token}] Error: {error.message}")
    hadRuntimeError = True

# Token

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

# Lexer

class Lexer():
    def __init__(self, code): # Lexer setup

        self.code = code

        self.KEYWORDS = ["PRINT"]                       # Další speciální

        self.tokens = [] # Veškeré tokeny
        self.chars = "" # momentální paměť
        self.cur = 0 # Pozice, kterou se zabývá lexer
        # code[self.cur] = character in CURrent position in CODE
    
    def peek(self, n): # O kolik znaků se podívat dál?
        peeked = ""
        peek_cur = self.cur
        while self.cur < len(self.code) and len(peeked) < n:
            peek_cur += 1
            peeked += self.code[peek_cur]
        return peeked

    def gettokens(self) -> list[Tkn]:  # Pravý lexer

        # Token: (Name, Object, Line)

        while self.cur < len(self.code):
    
            if self.code[self.cur].isalpha():         # Keywordy a identifikátory
                while self.cur < len(self.code) and self.code[self.cur].isalnum():
                    self.chars += self.code[self.cur]
                    self.cur += 1
                if self.chars.upper() in self.KEYWORDS:
                    self.tokens.append((self.chars.upper(), self.chars))
                else:
                    error(self.cur, f"Invalid text.")
        
            elif self.code[self.cur].isnumeric():
                while self.cur < len(self.code) and self.code[self.cur].isnumeric():
                    self.chars += self.code[self.cur]
                    self.cur += 1
                self.tokens.append(("NUMBER", float(self.chars)))
            
            elif self.code[self.cur] == '"':        # Stringy
                self.cur += 1
                while self.cur < len(self.code) and self.code[self.cur] != '"':
                    self.chars += self.code[self.cur]
                    self.cur += 1
                self.cur += 1
                self.tokens.append(("STRING", self.chars))
    
            elif self.code[self.cur] == ";":          # Konec statementu
                self.tokens.append(("SEMICOLON", ";"))
                self.cur += 1
            
            elif self.code[self.cur] == "/":         # Komentáře / Děleno
                if self.peek(2) == "//":
                    self.cur += 3
                    while self.cur < len(self.code) and "///" not in self.chars:
                            self.chars += self.code[self.cur]
                            self.cur += 1
                    self.cur += 1
                
                elif self.peek(1) == "/":
                    self.cur += 2
                    while self.cur < len(self.code) and self.code[self.cur] != "\n": self.cur += 1
                else: #NEZAPOMENOUT TO UDĚLAT I PRO /// !!!!!!
                      # dw už to tam je
                    self.tokens.append(("SLASH", "/"))
                    self.cur += 1
            
            elif self.code[self.cur] == "*":
                self.tokens.append(("STAR", "*"))
                self.cur += 1
    
            elif self.code[self.cur] == "=":
                if self.peek(1) == "=":
                    self.cur += 2
                    self.tokens.append(("EQUAL_EQUAL", "=="))
                else:
                    self.tokens.append(("EQUAL", "="))
                    self.cur += 1
            
            elif self.code[self.cur] == "!":
                if self.peek(1) == "=":
                    self.cur += 2
                    self.tokens.append(("EXCL_EQUAL", "!="))
                else:
                    self.tokens.append(("EXCL", "!"))
                    self.cur += 1
            
            elif self.code[self.cur] == ">":
                if self.peek(1) == "=":
                    self.cur += 2
                    self.tokens.append(("GREAT_EQUAL", ">="))
                else:
                    self.tokens.append(("GREAT", ">"))
                    self.cur += 1
            
            elif self.code[self.cur] == "<":
                if self.peek(1) == "=":
                    self.cur += 2
                    self.tokens.append(("LESS_EQUAL", "<="))
                else:
                    self.tokens.append(("LESS", "<"))
                    self.cur += 1
            
            elif self.code[self.cur] == "+":
                self.tokens.append(("PLUS", "+"))
                self.cur += 1
            
            elif self.code[self.cur] == "-":
                self.tokens.append(("MINUS", "-"))
                self.cur += 1
        
            elif self.code[self.cur] == "(":
                self.tokens.append(("L_PARENS", "("))
                self.cur += 1

            elif self.code[self.cur] == ")":
                self.tokens.append(("R_PARENS", ")"))
                self.cur += 1
            
            elif self.code[self.cur] == "{":
                self.tokens.append(("L_BRACE", "{"))
                self.cur += 1

            elif self.code[self.cur] == "}":
                self.tokens.append(("R_BRACE", "}"))
                self.cur += 1
            
            elif self.code[self.cur] == "[":
                self.tokens.append(("L_BRACKET", "["))
                self.cur += 1

            elif self.code[self.cur] == "]":
                self.tokens.append(("R_BRACKET", "]"))
                self.cur += 1
            
            elif self.code[self.cur] == ",":
                self.tokens.append(("COMMA", ","))
                self.cur += 1
        
            elif self.code[self.cur] == " " or self.code[self.cur] == "\n" or self.code[self.cur] == "\t":
                self.cur += 1

            else: # Pro mezery/ostatní znaky ignorovat zatim
                error(self.cur, f"Invalid Character \"{self.code[self.cur]}\"")
                self.cur += 1

            self.chars = ""
    
        self.tokens.append(("EOF", None))
        
        return self.tokens

if __name__ == "__main__":
    code = "print +1\n\"Hello World!\""
    lexer = Lexer(code)
    print(lexer.gettokens())