from sys import stdout

from parse import parse, remove_parenthesis

if __name__ != "__main__":
    import logger_conf

    logger = logger_conf.Log.logger


def eval_int(expression: list):
    """Evaluates an integer expression, where the input is a parsed list of tokens."""
    expression = remove_parenthesis(expression)
    logger.debug("Int Input: " + str(expression))
    length = len(expression)
    # expression is: empty (should not happen)
    if length == 0:
        return None

    # expression is: single-operand
    if length == 1:
        # should be an operand
        logger.debug(" Expression Return " + str(expression[0][0]))
        return expression[0][0]

    # expression is: left-expression main-operator right-expression

    operator_index = find_operator(expression)

    left_expression = expression[:operator_index]
    logger.debug(" Left Operand : " + str(left_expression))
    right_expression = expression[operator_index + 1:]
    logger.debug(" Right Operand : " + str(right_expression))
    main_operator = expression[operator_index]
    logger.debug(" Operator : " + str(main_operator))

    if main_operator[0] == '+':
        return eval_int(left_expression) + eval_int(right_expression)
    elif main_operator[0] == '-':
        return eval_int(left_expression) - eval_int(right_expression)
    elif main_operator[0] == '*':
        return eval_int(left_expression) * eval_int(right_expression)
    elif main_operator[0] == "/":
        return eval_int(left_expression) // eval_int(right_expression)


def find_operator(expression):
    """Find the operator where to split an integer expression in two operands."""
    parenthesis = 0
    # Check for + or -
    for i in range(len(expression)):
        if expression[i][1] == "parenthesis":
            if expression[i][0] == '(':
                parenthesis += 1
            else:
                parenthesis -= 1
        elif expression[i][1] == "operator":
            if expression[i][2] == 2 and parenthesis == 0:
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
    # @Thibault : What is what? Useless If (Dangerous)
    # if expression[i - 1][1] == "operator":
    #     return i - 1
    else:
        logger.error("Error: couldn't find operator. " + str(expression))
        raise Exception("Error: couldn't find operator.")


if __name__ == "__main__":
    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
    formatter.datefmt = "%H:%M:%S"
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Starting logger from module.")

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
            ("((1+(2*3))*(4*5))", "140"),
            ("(4+6)-5*9", "-35")]
    for e in range(len(test)):
        if str(eval_int(parse(test[e][0]))) == str(test[e][1]):
            logger.info(f"Succes {e}: {test[e][0]} = {test[e][1]}")
        else:
            logger.info(f"Failure {e}: {test[e][0]} != {test[e][1]}")
            logger.info(f" => Result: {eval_int(parse(test[e][0]))}")
            logger.info(f" => eval : {eval(test[e][0])}")
