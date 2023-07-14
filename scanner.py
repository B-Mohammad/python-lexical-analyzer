import re


class Token:
    def __init__(self, token_type, value, line, column):
        self.token_type = token_type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        return f'{self.line}\t{self.column}\t{self.value}\t{self.token_type}'

    def __repr__(self):
        return self.__str__()


class UnknownTokenError(Exception):

    def __init__(self, buffer, position):
        super().__init__()
        self.buffer = buffer
        self.position = position

    def __str__(self):
        return f'\nLexerError: Unknown token!\n\n▼\n{self.buffer[self.position:self.position + 30]}'


class Scanner:
    def __init__(self, rules, buffer):
        rules_list = [f'(?P<{typ}>{reg})' for typ, reg in rules]
        self.regex = re.compile('|'.join(rules_list))
        self.buffer = buffer
        self.line = 1
        self.column = 1
        self.position = 0  
        self.newline_indexes = [i for i, c in enumerate(buffer) if c == '\n']
        self.newline_indexes.append(len(buffer))

    def token(self):
        if self.position < len(self.buffer):
            if match := re.compile('\S').search(self.buffer, self.position):
                self.position = match.start()
            else:
                return None

            for line, pos in enumerate(self.newline_indexes):
                if self.position < pos:
                    self.line = line + 1
                    if line == 0:
                        self.column  = self.position + 1
                    else:
                        self.column = self.position - self.newline_indexes[line-1]
                    break

            if match := self.regex.match(self.buffer, self.position):            
                token = Token(token_type=match.lastgroup, value=match.group(match.lastgroup), line=self.line, column=self.column)
                self.position = match.end()
                return token
            else:
                raise UnknownTokenError(self.buffer, self.position)
    
    def token_generator(self):
        self.position = 0
        while token := self.token():
            yield token