from contextlib import contextmanager
from tabulate import tabulate
from colorama import Fore

from cases_creator import CasesCreator


@contextmanager
def padding():
    try:
        yield print()
    finally:
        print()


while True:
    text = input('> ')
    cases = CasesCreator(text)

    def format_cases():
        for i in cases:
            input_data, result = i
            yield [*input_data, result]

    try:
        result = list(format_cases())

        if len(result) == 1:
            print(result[0][0])
        else:
            with padding():
                print(tabulate(result, headers=[*cases.literals, 'result']))
    except Exception as e:
        print(Fore.RED + str(e) + Fore.RESET)
        print()
