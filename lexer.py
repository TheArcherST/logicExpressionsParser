import typing
from dataclasses import dataclass

from colorama import Style


class TokenTypes:
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'

    NOT = 'NOT'
    AND = 'AND'
    OR = 'OR'
    IMPLICATION = 'IMPLICATION'
    EQUALITY = 'EQUALITY'

    BOOL = 'BOOL'

    EOF = 'EOF'


class OperationTypes:
    FACTOR = 'FACTOR'
    BINARY = 'BINARY'
    UNARY = 'UNARY'
    EOF = 'EOF'


@dataclass
class Token:
    type: str
    op_type: str
    value: typing.Optional[typing.Union[str, bool]]
    real_position: int = None

    def visualize_location(self, text: str, marker='') -> str:
        if self.type == TokenTypes.EOF:
            self.real_position = len(text) + 2

        result = text + '\n'
        result += ' ' * (self.real_position - 1) + marker + '^' + Style.RESET_ALL

        return result


class Lexer:
    def __init__(self, text: str):
        self.text = text

    @staticmethod
    def normalize_text(text: str):
        def unplug(literals: list[str], text_: str):
            for literal in literals:
                text_ = text_.replace(literal, f' {literal} ')

            return text_

        # if operators concatenated to id, will be unplugged
        # but can be generated double spaces
        text = unplug(['!', '(', ')', '&', '||', '->', '=='], text)

        # rm all double spaces
        while text.find('  ') != -1:
            text = text.replace('  ', ' ')
        
        return text

    def iterator(self) -> typing.Generator[Token, None, None]:
        text = self.normalize_text(self.text)
        position = 0
        div_literal = ' '
        for i in text.split(div_literal):
            token = self._token_factory(i, position)
            yield token
            position += len(i) + len(div_literal)

    @staticmethod
    def _token_factory(text: str, real_position: int = None) -> Token:
        result = None

        if text == '&':
            result = Token(TokenTypes.AND, OperationTypes.BINARY, text, real_position)
        elif text == '||':
            result = Token(TokenTypes.OR, OperationTypes.BINARY, text, real_position)
        elif text == '!':
            result = Token(TokenTypes.NOT, OperationTypes.UNARY, text, real_position)
        elif text == '->':
            result = Token(TokenTypes.IMPLICATION, OperationTypes.BINARY, text, real_position)
        elif text == '==':
            result = Token(TokenTypes.EQUALITY, OperationTypes.BINARY, text, real_position)
        elif text == '(':
            result = Token(TokenTypes.LPAREN, OperationTypes.FACTOR, text, real_position)
        elif text == ')':
            result = Token(TokenTypes.RPAREN, OperationTypes.FACTOR, text, real_position)
        elif text in ('true', '1'):
            result = Token(TokenTypes.BOOL, OperationTypes.FACTOR, True, real_position)
        elif text in ('false', '0'):
            result = Token(TokenTypes.BOOL, OperationTypes.FACTOR, False, real_position)
        elif text == '':
            result = Token(TokenTypes.EOF, OperationTypes.EOF, None)

        if result:
            return result
        else:
            raise KeyError(f'Lexer: name {text} not found')

    @classmethod
    def get_unknown_names(cls, text: str) -> list[str]:
        result: list[str] = []

        text = cls.normalize_text(text)
        for i in text.split():
            try:
                cls._token_factory(i)
            except KeyError:
                result.append(i)

        return list(set(result))
