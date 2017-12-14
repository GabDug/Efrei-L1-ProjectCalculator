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
    leftExpression = expression[:find_operator(expression)]
    print(" Left Operand : " + str(leftExpression))
    rightExpression = expression[find_operator(expression)+1:]
    print(" Right Operand : ", rightExpression)
    mainOperator = expression[find_operator(expression)]
    print(" Operator : ", mainOperator)

    if mainOperator[0] == '+':
        return eval_int(leftExpression) + eval_int(rightExpression)
    elif mainOperator[0] == '-':
        return eval_int(leftExpression) - eval_int(rightExpression)
    elif mainOperator[0] == '*':
        return eval_int(leftExpression) * eval_int(rightExpression)
    elif mainOperator[0] == "/":
        return eval_int(leftExpression) // eval_int(rightExpression)


def find_operator(expression):
    parenthesis = 0
    i = 0
    for i in range(len(expression)):
        if expression[i][1] == "parenthesis":
            if expression[i][0] == '(':
                parenthesis += 1
            else:
                parenthesis -= 1
        elif expression[i][1] == "operator":
            if expression[i][2] == 0 and parenthesis == 0:
                return i
    if expression[i - 1][1] == "operator":
        return i - 1
    else:
        return None


def remove_parenthesis(expression):
    if expression[0][0] == '(' and expression[-1][0] == ')':
        return expression[1:-1]


if __name__ == "__main__":
    print("1, ", eval_int(parse("3*2+5")))
    print("2, ", eval_int(parse("5+2*3")))
    print("3, ", eval("5+2*3"))

    # print(find_operator(parse("(1 + 1) * 4")))
