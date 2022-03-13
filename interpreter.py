import typing
from colorama import Fore

from lexer import Lexer, Token, TokenTypes, OperationTypes


def implication(x, y):
    return (not x).__or__(y)


EOF = Token(TokenTypes.EOF, OperationTypes.EOF, None)
_T = typing.TypeVar('_T')


class Interpreter:
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.tokens_iterator = self.lexer.iterator()
        self.current_token = EOF
        self.previous_token = EOF

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
            self._report_runtime_error(self.current_token, token_type)

    def expr(self):
        result = self.eq_()
        return result

    def eq_(self):
        result = self._check_result(self.smpl_())

        while self.current_token.type == TokenTypes.EQUALITY:
            self.eat(TokenTypes.EQUALITY)
            factor = self.smpl_()
            result = result == factor

        return result

    def smpl_(self):
        result = self._check_result(self.or_())

        while self.current_token.type == TokenTypes.IMPLICATION:
            self.eat(TokenTypes.IMPLICATION)
            factor = self.or_()
            result = implication(result, factor)

        return result

    def or_(self):
        result = self._check_result(self.and_())

        while self.current_token.type == TokenTypes.OR:
            self.eat(TokenTypes.OR)
            factor = self.and_()
            result = result.__or__(factor)

        return result

    def and_(self):
        result = self._check_result(self.not_())

        while self.current_token.type == TokenTypes.AND:
            self.eat(TokenTypes.AND)
            factor = self.not_()
            result = result and factor

        return result

    def not_(self):
        result = self._check_result(self.factor())

        while self.current_token.type == TokenTypes.NOT:
            self.eat(TokenTypes.NOT)
            factor = self.factor()
            result = not factor

        return result

    def factor(self):
        token = self._check_result(self.current_token)

        if token.type == TokenTypes.BOOL:
            self.eat(TokenTypes.BOOL)
            result = token.value

        elif token.type == TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            result = self.expr()
            self.eat(TokenTypes.RPAREN)
        elif token.type == TokenTypes.EOF:
            result = None
        else:
            result = None

        return result

    def _report_runtime_error(self, invalid_token: Token, excepted_type: str = None) -> None:
        text = self.lexer.text

        if (invalid_token.real_position is None) & (invalid_token.type != TokenTypes.EOF):
            print('Not located runtime error')
        else:
            print('\n' + invalid_token.visualize_location(self.lexer.text, marker=Fore.RED))

        if excepted_type is not None:
            print(f'Excepted token `{excepted_type}`, but `{invalid_token.type}` got')

    def _check_result(self, data: _T) -> _T:
        if self.previous_token.op_type in (OperationTypes.BINARY, OperationTypes.UNARY):
            if not data.type == TokenTypes.BOOL:
                self._report_runtime_error(data, TokenTypes.BOOL)

        return data
