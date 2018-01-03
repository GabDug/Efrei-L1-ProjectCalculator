# from eval_str import eval_str
from parse import parse, remove_parenthesis

if __name__ != "__main__":
    import logging

    logger = logging.getLogger(__name__)


def single_element(element: tuple):
    """Evaluate a single token. Used when there is only one token."""
    if element[1] == "variable":
        if element[0] == "exit":
            logger.info("Exiting...")
            exit()
    elif element[1] == "integer":
        return element[0]
    elif element[1] == "string":
        return element[0]
    elif element[1] == "boolean":
        return element[0]


def first_eval(expression: list):
    """Evaluates an expression (boolean, integer or string), where the input is a parsed list of tokens."""
    size = len(expression)
    if size == 0:
        # TODO According to the subject, the program should quit if the user press enter twice, so we should add a
        # variable for this
        # logger.info("Exiting...")
        # exit()
        raise Exception('Error: Expression is empty.')
    elif size == 1:
        return single_element(expression[0])
    else:
        return eval_global(expression)


def eval_global(expression: list):
    """Evaluates an expression, where the input is a parsed list of tokens."""
    expression = remove_parenthesis(expression)
    logger.debug("Input at eval global: " + str(expression))
    length = len(expression)
    # expression is: empty (should not happen)
    if length == 0:
        raise Exception("   Error: expression is empty.")

    # expression is: single-operand
    if length == 1:
        # should be an operand
        if expression[0] == True:
            logger.debug("  Return: true")
            return "true"
        if not expression[0]:
            logger.debug("  Return: false")
            return "false"

        logger.debug("  Return:" + str(expression[0][0]))
        return expression[0][0]

    # Expression Shape: left-expression main-operator right-expression
    operator_index = find_operator(expression)
    logger.debug("  Operator Index: " + str(operator_index))

    left_expression = expression[:operator_index]
    logger.debug(" Left Operand: " + str(left_expression))
    right_expression = expression[operator_index + 1:]
    logger.debug(" Right Operand: " + str(right_expression))
    main_operator = expression[operator_index]
    logger.debug(" Operator: " + str(main_operator))

    # Prefix unary operator, right side of expression
    if expression[operator_index][0] == "not":
        logger.debug("  In Not Process:")

        if left_expression is None or left_expression == []:
            logger.debug("      Left Expression Is None")
            if eval_global(right_expression) == "true":
                logger.debug("    Return: false")
                return "false"
            else:
                logger.debug("    Return: true")
                return "true"
        else:
            logger.debug("      Left Exp     : " + str(left_expression))

            if eval_global(right_expression) == "true":
                left_expression.append(("false", "boolean"))
            else:
                left_expression.append(("true", "boolean"))
            logger.debug("  Return eval: " + str(left_expression))
            return eval_global(left_expression)

    # Binary infix operators
    else:
        if main_operator[0] == '+':
            return eval_global(left_expression) + eval_global(right_expression)
        elif main_operator[0] == '-':
            return eval_global(left_expression) - eval_global(right_expression)
        elif main_operator[0] == '*':
            return eval_global(left_expression) * eval_global(right_expression)
        elif main_operator[0] == "/":
            return eval_global(left_expression) // eval_global(right_expression)
        elif main_operator[0] == '==':
            if eval_global(left_expression) == eval_global(right_expression):
                return "true"
            else:
                return "false"
                # return eval_global(left_expression) == eval_global(right_expression)
        elif main_operator[0] == '!=':
            if eval_global(left_expression) != eval_global(right_expression):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '<':
            if eval_global(left_expression) < eval_global(right_expression):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '>':
            if eval_global(left_expression) > eval_global(right_expression):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '<=':
            if eval_global(left_expression) <= eval_global(right_expression):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '>=':
            if eval_global(left_expression) >= eval_global(right_expression):
                return "true"
            else:
                return "false"
        elif main_operator[0] == 'and':
            if eval_global(left_expression) == eval_global(right_expression) == 'true':
                return "true"
            else:
                return "false"
        elif main_operator[0] == 'or':
            if eval_global(left_expression) == "true" or eval_global(right_expression) == 'true':
                return "true"
            else:
                return "false"
                # def eval_variable(expression: list):
                #     """Evaluates the variables."""
                #     TODO pas fini
                #     size = len(expression)
                #
                #     i = 0
                #     while i < size:
                #         if expression[i][0] == "variable":
                #             eval_exp = first_eval()


def ext_eval_global(expression_str: str):
    """Evaluates an expression (boolean, integer or string), where the input is a string."""
    return first_eval(parse(expression_str))


def find_operator(expression):
    """Find the operator where to split an integer expression in two operands."""
    parenthesis = 0
    # Check for + or -
    for j in range(6, -1, -1):
        for i in range(len(expression) - 1, -1, -1):
            if expression[i][1] == "parenthesis":
                if expression[i][0] == '(':
                    parenthesis += 1
                else:
                    parenthesis -= 1
            elif expression[i][1] == "operator":
                if expression[i][2] == j and parenthesis == 0:
                    return i


if __name__ == "__main__":
    import logger_conf

    logger = logger_conf.Log.logger

    print(ext_eval_global("'Hi' < 'Hello'"))
    # print(ext_eval_global("false and false"))
    # print(ext_eval_global("false and false"))
    # print(ext_eval_global("true and false"))
    # print(ext_eval_global("true and true"))
    # print(ext_eval_global("false and true"))
    # print(ext_eval_global("false or false"))
    # print(ext_eval_global("true or false"))
    # print(ext_eval_global("true or true"))
    # print(ext_eval_global("false or true"))
    # print(ext_eval_global("not true"))
    # print(ext_eval_global("not false"))
    # print(ext_eval_global("not not true"))
    # print(ext_eval_global("not not false"))
    # print(ext_eval_global("not not not true"))
    # print(ext_eval_global("not not not false"))
    #
    # print(ext_eval_global("-35 == (4+6)-5*9"))
    # print(ext_eval_global("1==2"))
    # print(ext_eval_global("1+2 == 3"))
    # print(ext_eval_global("2 == 1+1"))
    # print(ext_eval_global("(false)"))
    # print(ext_eval_global("true"))
    # test = [("1",),
    #         ("(1)",),
    #         ("1 - 2",),
    #         ("4 / 2 * 3",),
    #         ("4 * 2 / 3",),
    #         ("(1 + 2) * 3",),
    #         ("-1 + -1 + (-1 - -1)",),
    #         ("((1+(2*3))*(4*5))",),
    #         ("(4+6)-5*9",)]
    # for e in range(len(test)):
    #     # if str(parse(test[e][0])) == str(test[e][1]):
    #     logger.warning(f"Clean {e}: {test[e][0]}")
    #
    #     logger.warning(f" => Result: {(parse(test[e][0]))}")
    #
    # test = [("1", "1"),
    #         ("(1)", "1"),
    #         ("1 - 2", "-1"),
    #         ("4 / 2 * 3", "6"),
    #         ("4 * 2 / 3", "2"),
    #         ("1 + 2 * 3", "7"),
    #         ("(1 + 2) * 3", "9"),
    #         ("-1 + -1 + (-1 - -1)", "-2"),
    #         ("-1 + -1 - (-1 - -1)", "-2"),
    #         ("(-1 + -1 - (-1 - -1))", "-2"),
    #         ("((-1 + -1 - (-1 - -1)))", "-2"),
    #         ("((1+(2*3))*(4*5))", "140"),
    #         ("(4+6)-5*9", "-35")]
    # for e in range(len(test)):
    #     if str(eval_global(parse(test[e][0]))) == str(test[e][1]):
    #         logger.info(f"Succes {e}: {test[e][0]} = {test[e][1]}")
    #     else:
    #         logger.error(f"Failure {e}: {test[e][0]} != {test[e][1]}")
    #         logger.info(f" => Result: {eval_global(parse(test[e][0]))}")
    #         logger.info(f" => eval : {eval(test[e][0])}")
