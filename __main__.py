from tabulate import tabulate
from colorama import Fore

from cases_creator import CasesCreator


while True:
    text = input('statement: ')
    cases = CasesCreator(text)

    def format_cases():
        for i in cases:
            input_data, result = i
            yield [*input_data, result]

    try:
        print(tabulate(format_cases(), headers=[*cases.literals, 'result']))
    except Exception as e:
        print(Fore.RED + str(e) + Fore.RESET)

    print()
