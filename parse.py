import re


def _expression_to_list(expression: str) -> list:
    # return re.split("([()+-/*])", expression.replace(" ", ""))
    return re.findall('[0-9.]+|[+\-*^/()]', expression.replace(" ", ""))


def _get_tuple(token: str, index: int) -> tuple:
    """Returns a tuple for each token.
    First value is the token,
    Second value is the kind of token,
    (Optional) Third value is:  for operators: the priority (0 is the highest)
                                for parenthesis: the index of the couple opening parenthesis
    """
    if token in "+-":
        return token, "operator", 0
    elif token in "*/":
        return token, "operator", 1
    elif token in "()":
        global parenthesis_stack
        if token == "(":
            parenthesis_stack.append(index)
            parenthesis_id = index
        elif token == ")":
            parenthesis_id = parenthesis_stack[-1]
            del parenthesis_stack[-1]
        return token, "parenthesis", parenthesis_id
    else:
        try:
            return int(token), "integer"
        except ValueError:
            return token, "unknown"


def parse(expression: str) -> list:
    """Parse a string expression to a list of tuples."""
    list_expression = _expression_to_list(expression)
    final_list = []
    global parenthesis_stack
    parenthesis_stack = []

    for i in range(len(list_expression)):
        tup = _get_tuple(list_expression[i], i)
        # Check nagative integer
        if tup[1] == "integer" and i != 0 and final_list[-1][0] == "-":
            if i == 1 or final_list[-2][1] != "integer":
                del final_list[-1]
                tup = (-1 * tup[0], tup[1])
                final_list.append(tup)
            else:
                final_list.append(tup)
        else:
            final_list.append(tup)
    return final_list


if __name__ == "__main__":
    # print(parse("3+4*2"))
    # print(parse("(3 + 2) * 4"))
    # print(parse("3 - 4"))
    # print(parse("-4 + 3"))
    # print(parse("(-1) + -1 + (-1 - -1)"))
    # print(parse("(3+254)* 44 "))
    print(parse("((1))"))
    print(parse("(1)*(2)"))
    print(parse("(1+(2*3))"))
    print(parse("(1+(2*3))(4*5)"))
    print(parse("((1+(2*3))(4*5))"))
