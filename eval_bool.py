from parse import parse, remove_parenthesis

if __name__ != "__main__":
    import logger_conf

    logger = logger_conf.Log.logger


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
        logger.error("Error: couldn't find operator. " + str(expression))
        raise Exception("Error: couldn't find operator.")


def eval_bool(expression):
    pass
