import re


def _expression_to_list(expression: str) -> list:
    # return re.split("([()+-/*])", expression.replace(" ", ""))
    return re.findall('[0-9.]+|[+\-*^/()]', expression.replace(" ", ""))


def _get_tuple(token: str) -> tuple:
    if token in "+-":
        return token, "operator", 0
    elif token in "*/":
        return token, "operator", 1
    elif token in "()":
        global parenthesis_counter
        if token == "(":
            parenthesis_counter += 1
            parenthesis_id = parenthesis_counter
        elif token == ")":
            parenthesis_counter -= 1
            parenthesis_id = parenthesis_counter - 1
        return token, "parenthesis", parenthesis_id
    else:
        try:
            return int(token), "integer"
        except ValueError:
            return token, "unknown"


def parse(expression: str) -> list:
    list_expression = _expression_to_list(expression)
    global parenthesis_counter
    parenthesis_counter = 0
    for i in range(len(list_expression)):
        list_expression[i] = _get_tuple(list_expression[i], parenthesis_counter)
    print(list_expression)
    return list_expression


if __name__ == "__main__":
    # print(parse("3+4*2"))
    # print(parse("(3 + 2) * 4"))
    print(parse(" ( 3+2 )* 4 "))
    print(parse("((3+(2))*4)"))
    # print(parse("(3+254)* 44 "))
