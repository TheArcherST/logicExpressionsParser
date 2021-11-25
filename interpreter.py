import typing

from lexer import Lexer, Token, TokenTypes, OperationTypes


def implication(x, y):
    return (not x).__or__(y)


class Interpreter:
    def __init__(self, text: str):
        self.tokens_iterator = Lexer(text).iterator()
        self.current_token = Token(TokenTypes.EOF, OperationTypes.EOF, None)
        self.previous_token = Token(TokenTypes.EOF, OperationTypes.EOF, None)

        self._next_token()

    def _next_token(self):
        self.previous_token = self.current_token

        try:
            self.current_token = self.tokens_iterator.__next__()
        except StopIteration:
            self.current_token = Token(TokenTypes.EOF, OperationTypes.EOF, None)

        return self.current_token

    def eat(self, token_type: str):
        if self.current_token.type == token_type:
            return self._next_token()
        else:
            self._raise_syntax_error(f'excepted token `{token_type}`')

    def expr(self):
        result = self.eq_()
        return result

    def eq_(self):
        result = self.smpl_()

        while self.current_token.type == TokenTypes.EQUALITY:
            self.eat(TokenTypes.EQUALITY)
            factor = self.smpl_()
            result = result == factor

        return result

    def smpl_(self):
        result = self.or_()

        while self.current_token.type == TokenTypes.IMPLICATION:
            self.eat(TokenTypes.IMPLICATION)
            factor = self.or_()
            result = implication(result, factor)

        return result

    def or_(self):
        result = self.and_()

        while self.current_token.type == TokenTypes.OR:
            self.eat(TokenTypes.OR)
            factor = self.and_()
            result = result.__or__(factor)

        return result

    def and_(self):
        result = self.not_()

        while self.current_token.type == TokenTypes.AND:
            self.eat(TokenTypes.AND)
            factor = self.not_()
            result = result and factor

        return result

    def not_(self):
        result = self.factor()

        while self.current_token.type == TokenTypes.NOT:
            self.eat(TokenTypes.NOT)
            factor = self.factor()
            result = not factor

        return result

    def factor(self):
        token = self.current_token

        if token.type == TokenTypes.BOOL:
            self.eat(TokenTypes.BOOL)
            result = token.value

        elif token.type == TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            result = self.expr()
            self.eat(TokenTypes.RPAREN)
            result = result

        elif token.type == TokenTypes.EOF:
            raise Exception(f'Interpreter: excepted factor, but {token.type} got')
        else:
            result = None

        return result

    @staticmethod
    def _raise_syntax_error(msg: str) -> typing.NoReturn:
        raise Exception(f'Invalid syntax: {msg}')
