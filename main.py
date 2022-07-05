from calc.calc import Calc


def _main():
    prompt = "Input the expression to evaluate: "
    calc = Calc(prompt_length=len(prompt))
    try:
        s = input(prompt)
        while s:
            calc.input = s
            try:
                print(f"> {calc.result}")
            except SyntaxError as se:
                print(se)

            s = input(f"\n{prompt}")
        else:
            print("quit")
    except EOFError:
        print("quit")


if __name__ == "__main__":
    _main()
