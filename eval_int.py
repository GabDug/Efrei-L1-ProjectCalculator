from parse import parse


def eval_int(expression):
    expression = remove_parenthesis(expression)
    print("Input : ", expression)
    length = len(expression)

    # expression is: empty (should not happen)
    if length == 0:
        return None

    # expression is: single-operand
    if length == 1:
        # should be an operand
        print(" Return ", expression[0][0])
        return expression[0][0]

    # expression is: left-expression main-operator right-expression
    left_expression = expression[:find_operator(expression)]
    print(" Left Operand : " + str(left_expression))
    right_expression = expression[find_operator(expression) + 1:]
    print(" Right Operand : ", right_expression)
    main_operator = expression[find_operator(expression)]
    print(" Operator : ", main_operator)

    if main_operator[0] == '+':
        return eval_int(left_expression) + eval_int(right_expression)
    elif main_operator[0] == '-':
        return eval_int(left_expression) - eval_int(right_expression)
    elif main_operator[0] == '*':
        return eval_int(left_expression) * eval_int(right_expression)
    elif main_operator[0] == "/":
        return eval_int(left_expression) // eval_int(right_expression)


def find_operator(expression):
    """Find the operator where to split an expression in two operands."""
    parenthesis = 0
    # Check for + or -
    for i in range(len(expression)):
        if expression[i][1] == "parenthesis":
            if expression[i][0] == '(':
                parenthesis += 1
            else:
                parenthesis -= 1
        elif expression[i][1] == "operator":
            if expression[i][2] == 0 and parenthesis == 0:
                return i
    # If none then check for * or /
    for i in range(len(expression)-1, -1, -1):
        if expression[i][1] == "parenthesis":
            if expression[i][0] == '(':
                parenthesis += 1
            else:
                parenthesis -= 1
        elif expression[i][1] == "operator":
            if expression[i][2] == 1 and parenthesis == 0:
                return i
    # @Thibault : What is what? Useless If (Dangerous)
    if expression[i - 1][1] == "operator":
        return i - 1
    else:
        print("Error: couldn't find main operator.")
        return None


def remove_parenthesis(expression):
    """Remove useless global parenthesis. Works recursively."""
    # If there is a parenthesis at beginning and at the end, and they are matching.
    if expression[0][0] == '(' and expression[-1][0] == ')' and expression[0][2] == expression[-1][2]:
        return remove_parenthesis(expression[1:-1])
    else:
        return expression


if __name__ == "__main__":
    test = [("1", "1"),
            ("(1)", "1"),
            ("1 - 2", "-1"),
            ("4 / 2 * 3", "6"),
            ("4 * 2 / 3", "2"),
            ("1 + 2 * 3", "7"),
            ("(1 + 2) * 3", "9"),
            ("-1 + -1 + (-1 - -1)", "-2"),
            ("-1 + -1 - (-1 - -1)", "-2"),
            ("(-1 + -1 - (-1 - -1))", "-2"),
            ("((-1 + -1 - (-1 - -1)))", "-2"),
            ("((1+(2*3))*(4*5))", "140")]
    for e in range(len(test)):
        if str(eval_int(parse(test[e][0]))) == str(test[e][1]):
            print(f"Succes {e}: {test[e][0]} = {test[e][1]}")
        else:
            print(f"Failure {e}: {test[e][0]} != {test[e][1]}")
            print(f" => Result: {eval_int(parse(test[e][0]))}")
            print(f" => eval : {eval(test[e][0])}")
