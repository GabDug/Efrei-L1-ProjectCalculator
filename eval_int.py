from parse import parse


def eval_int(expression):
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
    leftExpression = expression[:length - 2]
    print(" Left Operand : " + str(leftExpression))
    rightExpression = expression[length - 1:]
    print(" Right Operand : ", rightExpression)
    mainOperator = expression[length - 2]
    print(" Operator : ", mainOperator)

    if mainOperator[0] == '+':
        return eval_int(leftExpression) + eval_int(rightExpression)
    elif mainOperator[0] == '-':
        return eval_int(leftExpression) - eval_int(rightExpression)
    elif mainOperator[0] == '*':
        return eval_int(leftExpression) * eval_int(rightExpression)
    elif mainOperator[0] == "/":
        return eval_int(leftExpression) // eval_int(rightExpression)


if __name__ == "__main__":
    print("1,", eval_int(parse("3*2+5")))
    print("2,", eval_int(parse("2+5*3")))
    print("3, ", eval("3*2+5"))
