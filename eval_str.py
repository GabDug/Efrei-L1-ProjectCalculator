from parse import parse, remove_parenthesis


def eval_str(expression):
    expression = remove_parenthesis(expression)
    print("Str Input : ", expression)
    length = len(expression)

    # expression is: empty (should not happen)
    if length == 0:
        return None

    # expression is: single-operand
    if length == 1:
        # should be an operand
        # print(" Return ", expression[0][0])
        return expression[0][0]

    # expression is: left-expression main-operator right-expression
    left_expression = expression[:find_operator(expression)]
    right_expression = expression[find_operator(expression) + 1:]
    main_operator = expression[find_operator(expression)]
    # print(" Left Operand : " + str(left_expression))
    # print(" Right Operand : ", right_expression)
    # print(" Operator : ", main_operator)

    if main_operator[0] == '+':
        return eval_str(left_expression) + eval_str(right_expression)
    else:
        print("Error: no operator.")
        # If no operator, assume +
        return eval_str(left_expression) + eval_str(right_expression)


def find_operator(expression):
    """Find the operator where to split an expression in two operands."""
    parenthesis = 0
    # Check for +
    for i in range(len(expression)):
        if expression[i][1] == "parenthesis":
            if expression[i][0] == '(':
                parenthesis += 1
            else:
                parenthesis -= 1
        elif expression[i][1] == "operator":
            if expression[i][2] == 0 and parenthesis == 0:
                return i
    print("Error: couldn't find main operator.")
    return None


if __name__ == "__main__":
    print(eval_str(parse("'Hello'")))
    print(eval_str(parse("'Hello' + '' + 'world'")))
    print(eval_str(parse("'Hello' + ' ' + ('world' + '!')")))
