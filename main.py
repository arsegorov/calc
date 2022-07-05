from calc.calc import Calc


def _main():
    calc = Calc()
    try:
        calc.read_input()
        while calc.input:
            try:
                print(f"> {calc.result}")
            except SyntaxError as se:
                print(se)

            print()
            calc.read_input()
        else:
            print("quit")
    except EOFError:
        print("quit")


if __name__ == "__main__":
    _main()
