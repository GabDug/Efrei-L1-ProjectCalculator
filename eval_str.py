from parse import parse, remove_parenthesis

if __name__ != "__main__":
    import logger_conf

    logger = logger_conf.Log.logger


def eval_str(expression):
    expression = remove_parenthesis(expression)
    logger.debug("Str Input : ", expression)
    length = len(expression)

    # expression is: empty (should not happen)
    if length == 0:
        return None

    # expression is: single-operand
    if length == 1:
        # should be an operand
        # print(" Return ", expression[0][0])
        return expression[0][0]

    operator_index = find_operator(expression)

    left_expression = expression[:operator_index]
    logger.debug(" Left Operand : " + str(left_expression))
    right_expression = expression[operator_index + 1:]
    logger.debug(" Right Operand : " + str(right_expression))
    main_operator = expression[operator_index]
    logger.debug(" Operator : " + str(main_operator))

    if main_operator[0] == '+':
        return eval_str(left_expression) + eval_str(right_expression)
    else:
        logger.error("Error: couldn't find operator. " + str(expression))
        raise Exception("Error: couldn't find operator.")
        # OR
        # If no operator, assume +
        # return eval_str(left_expression) + eval_str(right_expression)


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
                # print("Error: couldn't find main operator.")
                # return None


if __name__ == "__main__":
    import logging
    from sys import stdout

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
    formatter.datefmt = "%H:%M:%S"
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Starting logger from module.")
    logger.info(eval_str(parse("'Hello'")))
    logger.info(eval_str(parse("'Hello' + '' + 'world'")))
    logger.info(eval_str(parse("'Hello' + ' ' + ('world' + '!')")))
