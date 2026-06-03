# Token class
# 
# Accepted names:
#     - string 
#     - lineref 
#     - offset 
#     - number    
#     - STATEMENT (see lexer class)
#     - identifier
#     - empty (whitespace)
#     - other (kept just in case, possible warn)
#     - EOF (end of file)
#     symbols:
#     - plus
#     - minus
#     - star
#     - slash

class Tkn():
    def __init__(self, name: str, value: object=None) -> None:
        self.name = name 
        self.value = value 
    
    def __repr__(self) -> str:
        return f"Token({self.name}: '{self.value if self.value != None else ""}')"

# Main lexer class

class Lexer():
    def __init__(self, source: str) -> None:
        self.keywords: list[str] = ["print", "write", "copy", "delete", "append", "goto", "if", "else", "endif", "export"]
        self.empties: list[str] = ["\t", " "]
        self.source = source 
        self.lines: list[list] = []
        self.char: int = 0
        self.charline: int = 0
        self.line: int = 0
        self.cur: str = ""
        self.tokens: list[Tkn] = []
    
    def scan(self) -> list:
        while self.notAtEnd():
            match self.peek():

                case "\"": # string
                    self.nextchar()
                    while self.notAtEnd() and self.peek() != "\"":
                        self.cur += self.peek()
                        self.nextchar()
                    self.nextchar()
                    self.tokens.append(Tkn("string", self.cur))

                case "#": # number
                    self.nextchar()
                    while self.notAtEnd() and self.peek().isnumeric():
                        self.cur += self.peek()
                        self.nextchar()
                    self.tokens.append(Tkn("number", int(self.cur)))
                
                case p if p.isnumeric(): # line reference
                    while self.notAtEnd() and self.peek().isnumeric():
                        self.cur += self.peek()
                        self.nextchar()
                    self.tokens.append(Tkn("lineref", int(self.cur)))
                
                case "+" | "-": # line offset / plus/mínus
                    self.cur += self.peek()
                    self.nextchar()
                    if self.peek() in self.empties:
                        self.tokens.append(Tkn("plus" if self.cur == "+" else "minus"))
                    elif self.peek().isnumeric():
                        while self.notAtEnd() and self.peek().isnumeric():
                            self.cur += self.peek()
                            self.nextchar()
                        self.tokens.append(Tkn("offset", int(self.cur)))
                    else:
                        self.error(f"[{self.line}:{self.char}]")
                
                case p if p.isalpha(): # statement / identifier
                    while self.notAtEnd() and self.peek().isalpha():
                        self.cur += self.peek()
                        self.nextchar()
                    if self.cur in self.keywords: self.tokens.append(Tkn(self.cur))
                    else: self.tokens.append(Tkn("identifier", self.cur))
                
                case "\t" | " ": # empty
                    while self.notAtEnd() and self.peek() == "\t" or self.peek() == " ":
                        self.cur += self.peek()
                        self.nextchar()
                    self.tokens.append(Tkn("empty", self.cur))

                case "\n": # handle newlines
                    self.line += 1
                    self.lines.append(self.tokens)
                    self.tokens = []
                    self.char += 1
                    self.charline = 0
            
                case _:   # we'll keep the unknown stuff just in case it's not actual code that's going to run but something else
                    self.tokens.append(Tkn("other", self.peek()))
                    self.nextchar()
        
            self.cur = ""
        
        self.tokens.append(Tkn("EOF"))
        self.lines.append(self.tokens)

        return self.lines

    def peek(self) -> str: 
        return self.source[self.char]
    
    def nextchar(self) -> None:
        self.char += 1
        self.charline += 1
    
    def peeknext(self) -> str:
        return self.source[self.char + 1]

    def notAtEnd(self) -> bool:
        return self.char < len(self.source)
    
    def error(self, problem):
        print(f"Error! {problem}")
        return

# Main function

def main() -> None:
    # Get the source

    source = '+24 -19\n1 + 3 + 0'

    # Lexer

    lexer = Lexer(source)
    lines = lexer.scan()

    # Stuff after the lexer

    print(lines)

if __name__ == "__main__":
    main()