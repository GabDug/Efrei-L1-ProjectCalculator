from eval_int import *


def single_element(element):
    if element[1] == "variable":
        if element[0] == "exit":
            exit()
        else:
            return element[3]
    elif element[1] == "integer":
        return element[0]


def eval_global(expression):
    size = len(expression)

    if size == 0:
        return None
    elif size == 1:
        return single_element(expression[0])

    else:
        return eval_int(expression)


if __name__ == "__main__":
    print(eval_global(parse("1")))
