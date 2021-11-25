import typing

from interpreter import Interpreter
from lexer import Lexer
from itertools import product


def replace_word(text: str, old__: str, new__: str):
    old__, new__ = str(old__), str(new__)

    text = f' {text} '

    while True:
        start = text.find(' ' + old__ + ' ')

        if start == -1:
            break

        spl = list(text)
        for num, i in enumerate(range(start + 1, start + len(old__) + 1)):
            spl[i] = new__[num]
        text = ''.join(spl)

    return text


class CasesCreator:
    """CasesCreator

    Input here statements with literal values and mark them

    """

    def __init__(self, text: str):
        self.text = text
        self.literals = Lexer.get_unknown_names(text)

    def __iter__(self) -> tuple[typing.Iterable[int], int]:
        sequence_len = len(self.literals)

        for i in product((0, 1), repeat=sequence_len):
            text = self.text
            text = Lexer.normalize_text(text)

            for k, v in zip(self.literals, i):
                text = replace_word(text, k, v)

            interpreter = Interpreter(text)

            yield i, interpreter.expr()

    def __str__(self):
        return str(list(self))

    __repr__ = __str__
