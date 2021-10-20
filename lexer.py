import typing
from dataclasses import dataclass


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


@dataclass
class Token:
    type: str
    value: typing.Optional[typing.Union[str, bool]]


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

    def iterator(self) -> typing.Generator:
        text = self.normalize_text(self.text)
        for i in text.split():
            token = self._token_factory(i)
            yield token

    @staticmethod
    def _token_factory(text: str) -> Token:

        result = None

        if text == '&':
            result = Token(TokenTypes.AND, text)
        elif text == '||':
            result = Token(TokenTypes.OR, text)
        elif text == '!':
            result = Token(TokenTypes.NOT, text)
        elif text == '->':
            result = Token(TokenTypes.IMPLICATION, text)
        elif text == '==':
            result = Token(TokenTypes.EQUALITY, text)
        elif text == '(':
            result = Token(TokenTypes.LPAREN, text)
        elif text == ')':
            result = Token(TokenTypes.RPAREN, text)
        elif text in ('true', '1'):
            result = Token(TokenTypes.BOOL, True)
        elif text in ('false', '0'):
            result = Token(TokenTypes.BOOL, False)

        if result:
            return result
        else:
            raise KeyError(f'Name {text} not found')

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
