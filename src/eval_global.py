from os import system, name

from parse import parse, remove_parenthesis

if __name__ != "__main__":
    import logging

    logger = logging.getLogger(__name__)

unauthorized_var = ("exit", "clear", "not", "and", "or", "true", "false")


def _clear():
    system('cls' if name == 'nt' else 'clear')


def _single_element(element: tuple, variable_dic):
    """Evaluate a single token. Used when there is only one token."""
    if element[1] == "variable":
        if element[0] == "exit":
            logger.info("Exiting...")
            exit()
        elif element[0] == "clear":
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


def _get_single_element_type(element):
    """Returns the type of an element (bool, str, int...)"""
    if element == "false" or element == "true":
        return "boolean"
    elif isinstance(element, int):
        return "integer"
    else:
        return "string"


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
            left = _eval_global(left_expression, var_dic)
            left_type = _get_single_element_type(left)
            right = _eval_global(right_expression, var_dic)
            right_type = _get_single_element_type(right)
            if left_type != right_type:
                if left_type == "string" and right_type == "integer":
                    return left + str(right)
                elif left_type == "integer" and right_type == "string":
                    return str(left) + right
                else:
                    raise Exception(f"type mismatch ({left_type} {main_operator[0]} {right_type})")
            else:
                return left + right
        elif main_operator[0] == '-':
            try:
                return _eval_global(left_expression, var_dic) - _eval_global(right_expression, var_dic)
            except TypeError:
                raise Exception(f"type mismatch ({left_type} {main_operator[0]} {right_type})")
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


def ext_eval_global(expression_str: str, variable_dic=None):
    """Evaluates an expression (boolean, integer or string), where the input is a string."""
    return _first_eval(parse(expression_str), variable_dic)


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

    print(ext_eval_global("'Test' + 'string'"))
