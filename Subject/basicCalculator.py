# Parses a string containing the following tokens:
# - positive integer operands
# - integer operators + and -
# and returns the list of tokens tagged with their type.
#
# Tokens may be delimited by any number of blank characters.
#


def parse(string):
    # list of tokens to return
    tokens = []

    # go through the string
    i = 0
    length = len(string)
    while i < length:

        # skip blanks
        while i < length and string[i] == ' ':
            i += 1

        # look for integer operators
        if string[i] in "+-":
            operator = string[i]
            tokens += [(operator, "operator")]
            i += 1
            continue

            # look for integer operands
        if string[i] in "0123456789":
            j = i + 1
            while j < length and string[j] in "0123456789":
                j += 1
            operand = int(string[i:j])
            tokens += [(operand, 'operand')]
            i = j
            continue

    return tokens


# Evaluates an expression represented as a list of
# tagged tokens and returns the evaluation result.
#
# All operators are left-associative.
#
def evaluate(expression):
    length = len(expression)

    # expression is: empty (should not happen)
    if length == 0:
        return None

    # expression is: single-operand
    if length == 1:
        # should be an operand
        return expression[0][0]

    # expression is: left-expression main-operator right-expression
    leftExpression = expression[:length - 2]
    rightExpression = expression[length - 1:]
    mainOperator = expression[length - 2]

    if mainOperator[0] == '+':
        return evaluate(leftExpression) + evaluate(rightExpression)
    if mainOperator[0] == '-':
        return evaluate(leftExpression) - evaluate(rightExpression)


# Evaluates a sequence of user-input expressions.
#
def calculator():
    emptyCount = 0
    while True:

        # prompt for new expression
        line = input("? ")

        # check for empty line
        if line == "":
            emptyCount += 1
            if emptyCount == 2:
                break
            continue
        else:
            emptyCount = 0

        # evaluate expression and print result
        print(evaluate(parse(line)))

    print("done")


# Main program
#
calculator()
