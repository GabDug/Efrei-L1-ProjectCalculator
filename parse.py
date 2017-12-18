def _expression_to_list(expression: str) -> list:
    # return re.split("([()+-/*])", expression.replace(" ", ""))
    tokens = []

    i = 0
    length = len(expression)
    while i < length:
        if expression[i] == ' ':
            i += 1
            continue
        if expression[i] in "+-":
            tokens.append((expression[i], "operator", 0))
            i += 1
            continue
        if expression[i] in "/*":
            tokens.append((expression[i], "operator", 1))
            i += 1
            continue
        if expression[i] in "()":
            global parenthesis_stack
            if expression[i] == "(":
                parenthesis_stack.append(i)
                parenthesis_id = i
            elif expression[i] == ")":
                parenthesis_id = parenthesis_stack[-1]
                del parenthesis_stack[-1]
            tokens.append((expression[i], "parenthesis", parenthesis_id))
            i += 1
            continue
        if expression[i] in "0123456789":
            j = i + 1
            while j < len(expression) and expression[j] in "0123456789":
                j += 1
            tup = (int(expression[i:j]), "integer")

            # Here we check for negative numbers
            # TODO Stop working with tuple, better code
            if i != 0 and tokens[-1][0] == "-":
                if i == 1 or tokens[-2][1] != "integer":
                    # remove the operator
                    del tokens[-1]
                    tup = (-1 * tup[0], tup[1])
                    tokens.append(tup)
                else:
                    tokens.append(tup)
            else:
                tokens.append(tup)
            i = j
            continue
        if expression[i] in "'\"":
            j = i + 1
            while j < len(expression) and not expression[j] == expression[i]:
                j += 1
            if j == len(expression):
                print(" Error: no ending symbol for string")

            # i+1 to j : string without the starting and ending symbol
            tokens.append((expression[i + 1:j], "string"))
            # restart after the ending symbol (' or "...)
            i = j + 1
            continue
    print("=> ", tokens)
    return tokens


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
    print(list_expression)
    final_list = []
    global parenthesis_stack
    parenthesis_stack = []
    return list_expression


if __name__ == "__main__":
    # print(parse("3+4*2"))
    print(parse("248+345"))
    print(parse("(3 + 2) * 4"))
    print(parse("3 - 4"))
    print(parse("-4 + 3"))
    print(parse("(-1) + -1 + (-1 - -1)"))
    print(parse("(3+254)* 44 "))
    print(parse("'Yo'"))
    print(parse("'Hey''You'"))
    print(parse("'Test' + 'os'"))
    print(parse("'test"))
    print(parse("((1))"))
    print(parse("(1)*(2)"))
    print(parse("(1+(2*3))"))
    print(parse("(1+(2*3))(4*5)"))
    print(parse("((1+(2*3))(4*5))"))
