from eval_int import eval_int
from eval_str import eval_str
from parse import parse, remove_parenthesis


def single_element(element):
    if element[1] == "variable":
        if element[0] == "exit":
            print("Exiting...")
            exit()
        else:
            return element[3]
    elif element[1] == "integer":
        return element[0]
    elif element[1] == "string":
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
    print(eval_global(parse("exit")))
