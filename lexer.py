# Error reporting

hadError = False
hadRuntimeError = False

def error(line, character, item, message):
    report(line, character, "", message)

def report(line, character, item, message):
    global hadError
    print(f"[{line}:{character}] Error{item}: {message}")
    hadError = True

def runtimeError(error):
    global hadRuntimeError
    print(f"[{error.token}] Error: {error.message}")
    hadRuntimeError = True

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
        self.source = source            # Zdrojový kód
        self.lines: list[list] = []     # Veškeré řádky s lexémy
        self.char: int = 0              # Současný znak v programu
        self.charline: int = 0          # Současný znak v řádku
        self.line: int = 0              # Současný řádek
        self.cur: str = ""              # Současná forma lexému
        self.tokens: list[Tkn] = []     # Jeden současný řádek lexémů
    
    def scan(self) -> list[list]:
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
                        error(self.line, self.charline, "", f"{self.cur} must be followed by an empty character or a number.")
                
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
    
# Parser

class Parser():
    def __init__(self, lines) -> None:
        pass

# Main function

def main() -> None:
    # Get the source

    source: str = '+24 -19\n1 + 3 + 0'

    # Run the file/command

    run(source)

def run(src: str) -> None:
    global hadError

    # Lexer

    lexer: Lexer = Lexer(src)
    lines: list[list] = lexer.scan()

    # Parser

    parser: Parser = Parser(lines)

    statements = lines # placeholder

    if hadError or statements == None: return

    # Interpreter

    print(statements) # placeholder

if __name__ == "__main__":
    main()