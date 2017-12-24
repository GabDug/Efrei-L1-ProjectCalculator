from parse import parse, remove_parenthesis


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
    for i in range(len(expression) - 1, -1, -1):
        if expression[i][1] == "parenthesis":
            if expression[i][0] == '(':
                parenthesis += 1
            else:
                parenthesis -= 1
        elif expression[i][1] == "operator":
            if expression[i][2] == 1 and parenthesis == 0:
                return i
    else:
        print("Error: couldn't find main operator.")
        return None


def eval_bool(expression):
    pass
