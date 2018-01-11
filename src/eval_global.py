from os import system, name

from parse import parse, remove_parenthesis

if __name__ != "__main__":
    import logging

    logger = logging.getLogger(__name__)

unauthorized_var = ("exit", "_clear", "not", "and", "or", "true", "false")


def _clear():
    system('cls' if name == 'nt' else '_clear')


def _single_element(element: tuple, variable_dic):
    """Evaluate a single token. Used when there is only one token."""
    if element[1] == "variable":
        if element[0] == "exit":
            logger.info("Exiting...")
            exit()
        elif element[0] == "_clear":
            logger.info("Clear screen")
            _clear()
            return ""
        elif element[0] in variable_dic:
            return variable_dic[element[0]]
        else:
            raise Exception(f"unknown variable ('{element[0]}')")
    elif element[1] == "integer":
        return element[0]
    elif element[1] == "string":
        return element[0]
    elif element[1] == "boolean":
        return element[0]


def _eval_global(expression: list, var_dic: dict):
    """Evaluates an expression, where the input is a parsed list of tokens."""
    expression = remove_parenthesis(expression)
    logger.debug("Input at eval global: " + str(expression))
    length = len(expression)

    # If expression is empty (should not happen)
    if length == 0:
        raise Exception("expression is empty.")

    # If expression is single-operand (exit condition of recursivity)
    if length == 1:
        logger.debug("  Return:" + str(expression[0][0]))
        return _single_element(expression[0], var_dic)

    # Expression Shape: left-expression main-operator right-expression
    operator_index = find_operator(expression)
    logger.debug("  Operator Index: " + str(operator_index))
    if operator_index is None:
        raise Exception(f"missing operator")

    left_expression = expression[:operator_index]
    right_expression = expression[operator_index + 1:]
    main_operator = expression[operator_index]

    logger.debug(" Right Operand: " + str(right_expression))
    logger.debug(" Left Operand: " + str(left_expression))
    logger.debug(" Operator: " + str(main_operator))

    # If there is one side of the expression missing (except for unary prefix operators)
    if (left_expression == [] or right_expression == []) and main_operator[0] != "not":
        raise Exception(f"missing operand (near '{main_operator[0]}')")

    # Processing the prefix unary operator first, right side of expression
    if expression[operator_index][0] == "not":
        logger.debug("  Processing not")
        if left_expression is None or left_expression == []:
            if _eval_global(right_expression, var_dic) == "true":
                return "false"
            else:
                return "true"
        else:
            if _eval_global(right_expression, var_dic) == "true":
                left_expression.append(("false", "boolean"))
            else:
                left_expression.append(("true", "boolean"))
            return _eval_global(left_expression, var_dic)

    # Binary infix operators
    else:
        if main_operator[0] == '+':
            return _eval_global(left_expression, var_dic) + _eval_global(right_expression, var_dic)
        elif main_operator[0] == '-':
            return _eval_global(left_expression, var_dic) - _eval_global(right_expression, var_dic)
        elif main_operator[0] == '*':
            return _eval_global(left_expression, var_dic) * _eval_global(right_expression, var_dic)
        elif main_operator[0] == "/":
            return _eval_global(left_expression, var_dic) // _eval_global(right_expression, var_dic)
        elif main_operator[0] == '==':
            if _eval_global(left_expression, var_dic) == _eval_global(right_expression, var_dic):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '!=':
            if _eval_global(left_expression, var_dic) != _eval_global(right_expression, var_dic):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '<':
            if _eval_global(left_expression, var_dic) < _eval_global(right_expression, var_dic):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '>':
            if _eval_global(left_expression, var_dic) > _eval_global(right_expression, var_dic):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '<=':
            if _eval_global(left_expression, var_dic) <= _eval_global(right_expression, var_dic):
                return "true"
            else:
                return "false"
        elif main_operator[0] == '>=':
            if _eval_global(left_expression, var_dic) >= _eval_global(right_expression, var_dic):
                return "true"
            else:
                return "false"
        elif main_operator[0] == 'and':
            if _eval_global(left_expression, var_dic) == _eval_global(right_expression, var_dic) == 'true':
                return "true"
            else:
                return "false"
        elif main_operator[0] == 'or':
            if _eval_global(left_expression, var_dic) == "true" or _eval_global(right_expression, var_dic) == 'true':
                return "true"
            else:
                return "false"
        elif main_operator[0] == '=' and len(left_expression) != 1:
            raise Exception("variable assignment should be 'variable = exp'")
        elif main_operator[0] == '=' and left_expression[0][1] == "variable":
            if left_expression[0][0] in unauthorized_var:
                raise Exception("variable name can't be a reserved keyword")
            else:
                var_dic[left_expression[0][0]] = _eval_global(right_expression, var_dic)
                return ""
        # If we have "=" but the left side is not a variable
        elif main_operator[0] == '=' and left_expression[0][1] != "variable":
            raise Exception("variable name must start with a letter")


def _first_eval(expression: list, variable_dic):
    """Evaluates an expression (boolean, integer or string), where the input is a parsed list of tokens."""
    size = len(expression)
    if size == 0:
        raise Exception('Expression is empty.')
    elif size == 1:
        return _single_element(expression[0], variable_dic)
    else:
        return _eval_global(expression, variable_dic)


def ext_eval_global(expression_str: str, variable_list=None):
    """Evaluates an expression (boolean, integer or string), where the input is a string."""
    return _first_eval(parse(expression_str), variable_list)


def find_operator(expression):
    """Find the operator where to split an integer expression in two operands. We check from the end of the expression
    to the beggining (left associativity, from the lowest priority operator to the highest, ignoring operators in
    factors (between parenthesis)."""
    parenthesis = 0
    for j in range(7, -1, -1):
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
    import logging
    from sys import stdout

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
    formatter.datefmt = "%H:%M:%S"
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Starting logger from module.")

    # print(ext_eval_global("'Hi' < 'Hello'"))
    print(ext_eval_global("1 1"))
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
    #     if str(_eval_global(parse(test[e][0]))) == str(test[e][1]):
    #         logger.info(f"Succes {e}: {test[e][0]} = {test[e][1]}")
    #     else:
    #         logger.error(f"Failure {e}: {test[e][0]} != {test[e][1]}")
    #         logger.info(f" => Result: {_eval_global(parse(test[e][0]))}")
    #         logger.info(f" => eval : {eval(test[e][0])}")
