import re


def _expression_to_list(expression: str) -> list:
    # return re.split("([()+-/*])", expression.replace(" ", ""))
    return re.findall('[0-9.]+|[+\-*^/()]', expression.replace(" ", ""))


def _get_tuple(token: str) -> tuple:
    if token in "*+/-":
        return token, "operator"
    elif token in "()":
        return token, "parenthesis"
    else:
        try:
            return int(token), "integer"
        except ValueError:
            return token, "unknown"


def parse(expression: str) -> list:
    list_expression = _expression_to_list(expression)
    for i in range(len(list_expression)):
        list_expression[i] = _get_tuple(list_expression[i])
    return list_expression


if __name__ == "__main__":
    print(parse("(3 + 2) * 4"))
    print(parse(" ( 3+2 )* 4 "))
    print(parse("(3+254)* 44 "))
