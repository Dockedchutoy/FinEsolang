# Token class
# 
# Accepted names:
#     - string 
#     - lineref 
#     - offset 
#     - number    
#     - STATEMENT (see lexer class)
#     - empty (whitespace, comments)
#     - other (kept just in case, possible warn)
#     - EOF (end of file)

class Tkn():
    def __init__(self, name: str, value: object=None) -> None:
        self.name = name 
        self.value = value 
    
    def __repr__(self) -> str:
        return f"Token({self.name}: '{self.value if self.value != None else ""}')"

# Main lexer class

class Lexer():
    def __init__(self, source: str) -> None:
        self.keywords: list = ["print", "write", "copy", "delete", "append", "goto", "if", "else", "endif", "export"]
        self.source = source 
        self.lines: list[list] = []
        self.char: int = 0
        self.line: int = 0
        self.cur: str = ""
        self.tokens: list[Tkn] = []
    
    def scan(self) -> list:
        while self.notAtEnd():
            match self.peek():

                case "#": # number
                    self.char += 1
                    while self.notAtEnd() and self.peek().isnumeric():
                        self.cur += self.peek()
                        self.char += 1
                    self.tokens.append(Tkn("number", int(self.cur)))

                case "\"": # string
                    self.char += 1
                    while self.notAtEnd() and self.peek() != "\"":
                        self.cur += self.peek()
                        self.char += 1
                    self.char += 1
                    self.tokens.append(Tkn("string", self.cur))
                
                case "\n": # handle newlines
                    self.line += 1
                    self.lines.append(self.tokens)
                    self.tokens = []
                    self.char += 1
            
                case _:   # we'll keep the unknown stuff just in case it's not actual code that's going to run but something else
                    self.tokens.append(Tkn("other", self.peek()))
                    self.char += 1
        
            self.cur = ""
        
        self.tokens.append(Tkn("EOF"))
        self.lines.append(self.tokens)

        return self.lines

    def peek(self) -> str: 
        return self.source[self.char]

    def notAtEnd(self) -> bool:
        return self.char < len(self.source)

# Main function

def main() -> None:
    # Get the source

    source = '#1028\n"Hello World!"'

    # Lexer

    lexer = Lexer(source)
    lines = lexer.scan()

    # Stuff after the lexer

    print(lines)

if __name__ == "__main__":
    main()