from lexer import Lexer, Token, TokenTypes


def implication(x, y):
    return (not x).__or__(y)


class Interpreter:
    def __init__(self, text: str):
        self.tokens_iterator = Lexer(text).iterator()
        self.current_token = self._next_token()

    def _next_token(self):
        try:
            self.current_token = self.tokens_iterator.__next__()

        except StopIteration:
            self.current_token = Token(TokenTypes.EOF, None)

        return self.current_token

    def eat(self, token_type: str):
        if self.current_token.type == token_type:
            return self._next_token()
        else:
            raise Exception('Invalid syntax')

    def expr(self):
        result = self.eq_()
        return result

    def eq_(self):
        result = self.smpl_()

        while self.current_token.type == TokenTypes.EQUALITY:
            self.eat(TokenTypes.EQUALITY)
            result = result == self.smpl_()

        return result

    def smpl_(self):
        result = self.or_()

        while self.current_token.type == TokenTypes.IMPLICATION:
            self.eat(TokenTypes.IMPLICATION)
            result = implication(result, self.or_())

        return result

    def or_(self):
        result = self.and_()

        while self.current_token.type == TokenTypes.OR:
            self.eat(TokenTypes.OR)
            result = result.__or__(self.and_())

        return result

    def and_(self):
        result = self.not_()

        while self.current_token.type == TokenTypes.AND:
            self.eat(TokenTypes.AND)
            result = result and self.not_()

        return result

    def not_(self):
        result = self.factor()

        while self.current_token.type == TokenTypes.NOT:
            self.eat(TokenTypes.NOT)
            result = not self.factor()

        return result

    def factor(self):
        token = self.current_token
        if token.type == TokenTypes.BOOL:
            self.eat(TokenTypes.BOOL)

            return token.value
        elif token.type == TokenTypes.LPAREN:
            self.eat(TokenTypes.LPAREN)
            result = self.expr()
            self.eat(TokenTypes.RPAREN)

            return result
        elif token.type == TokenTypes.EOF:
            return None
