from os import system, name

from parse import parse, remove_parenthesis

if __name__ != "__main__":
    import logging

    logger = logging.getLogger(__name__)

unauthorized_var = ("exit", "clear", "not", "and", "or", "true", "false")


def _clear():
    system('cls' if name == 'nt' else 'clear')


def _check_variable(element: tuple, variable_dic):
    """Evaluate a single token. Used when there is only one token."""
    if element[1] == "variable":
        if element[0] == "exit":
            logger.info("Exiting...")
            exit()
        elif element[0] == "clear":
            logger.info("Clear screen")
            _clear()
            return "", "none"
        elif element[0] in variable_dic:
            return variable_dic[element[0]]
        else:
            raise Exception(f"unknown variable ('{element[0]}')")
    else:
        return element


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
        logger.debug("  Return:" + str(expression))
        return _check_variable(expression[0], var_dic)

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
    if (left_expression == [] or right_expression == []) and (main_operator[0] not in ["not", "-"]):
        raise Exception(f"missing operand (near '{main_operator[0]}')")

    right_eval = _eval_global(right_expression, var_dic)

    # Processing the prefix unary operator first, right side of expression
    if expression[operator_index][0] == "not":
        # right = _eval_global(right_expression, var_dic)
        if right_eval[1] == "boolean":
            if left_expression is None or left_expression == []:
                if right_eval[0] == "true":
                    return "false", "boolean"
                else:
                    return "true", "boolean"
            else:
                if right_eval[0] == "true":
                    left_expression.append(("false", "boolean"))
                else:
                    left_expression.append(("true", "boolean"))
                return _eval_global(left_expression, var_dic)
        else:
            raise Exception(f"type mismatch ({main_operator[0]} {right_eval[1]})")
    elif expression[operator_index][0] == "-" and expression[operator_index][2] == 0:
        right_eval = _eval_global(right_expression, var_dic)
        if right_eval[1] == "integer":
            right_eval = (-1 * right_eval[0], "integer")
            if left_expression is None or left_expression == []:
                return right_eval
            else:
                left_expression.append(right_eval)
                return _eval_global(left_expression, var_dic)
        else:
            raise Exception(f"type mismatch ({main_operator[0]} {right_eval[1]})")

    # Binary infix operators

    # First, the assignment because we don't evaluate the variable name (left)
    if main_operator[0] == '=' and len(left_expression) != 1:
        raise Exception("variable assignment should be 'variable = exp'")
    elif main_operator[0] == '=' and left_expression[0][1] == "variable":
        if left_expression[0][0] in unauthorized_var:
            raise Exception("variable name can't be a reserved keyword")
        else:
            var_dic[left_expression[0][0]] = right_eval
            return "", "none"
    # If we have "=" but the left side is not a variable
    elif main_operator[0] == '=' and left_expression[0][1] != "variable":
        raise Exception("variable name must start with a letter")

    # Then, all the operators that are binary (we evaluate
    left_eval = _eval_global(left_expression, var_dic)

    # For left and right:
    # [0] is the value
    # [1] is the type
    # [2] is the priority (exists if type operator)

    # Integer only operators
    if main_operator[0] in "%/-*":
        if left_eval[1] == right_eval[1] == "integer":
            if main_operator[0] == '*':
                return left_eval[0] * right_eval[0], "integer"
            elif main_operator[0] == "/":
                return left_eval[0] // right_eval[0], "integer"
            elif main_operator[0] == '-':
                return left_eval[0] - right_eval[0], "integer"
            elif main_operator[0] == '%':
                return left_eval[0] % right_eval[0], "integer"
        else:
            raise Exception(f"type mismatch ({left_eval[1]} {main_operator[0]} {right_eval[1]})")

    # Boolean only
    elif main_operator[0] in ["and", "or"]:
        if left_eval[1] == right_eval[1] == "boolean":
            if main_operator[0] == "and":
                if left_eval[0] == right_eval[0] == 'true':
                    return "true", "boolean"
                else:
                    return "false", "boolean"
            elif main_operator[0] == 'or':
                if left_eval[0] == "true" or right_eval[0] == 'true':
                    return "true", "boolean"
                else:
                    return "false", "boolean"
        else:
            raise Exception(f"type mismatch ({left_eval[1]} {main_operator[0]} {right_eval[1]})")

    # String and int only
    elif main_operator[0] in ["<", ">", "<=", ">="]:
        if (left_eval[1] == right_eval[1]) and (left_eval[1] == "integer" or left_eval[1] == "string"):
            if main_operator[0] == '<':
                if left_eval[0] < right_eval[0]:
                    return "true", "boolean"
                else:
                    return "false", "boolean"
            elif main_operator[0] == '>':
                if left_eval[0] > right_eval[0]:
                    return "true", "boolean"
                else:
                    return "false", "boolean"
            elif main_operator[0] == '<=':
                if left_eval[0] <= right_eval[0]:
                    return "true", "boolean"
                else:
                    return "false", "boolean"
            elif main_operator[0] == '>=':
                if left_eval[0] >= right_eval[0]:
                    return "true", "boolean"
                else:
                    return "false", "boolean"
        else:
            raise Exception(f"type mismatch ({left_eval[1]} {main_operator[0]} {right_eval[1]})")

    # Plus: str + str, int + int, or mixed
    elif main_operator[0] == '+':
        if left_eval[1] != right_eval[1]:
            if left_eval[1] == "string" and (right_eval[1] == "integer" or right_eval[1] == "boolean"):
                return left_eval[0] + str(right_eval[0]), "string"
            elif (left_eval[1] == "integer" or left_eval[1] == "boolean") and right_eval[1] == "string":
                return str(left_eval[0]) + right_eval[0], "string"
            else:
                raise Exception(f"type mismatch ({left_eval[1]} {main_operator[0]} {right_eval[1]})")
        elif left_eval[1] == right_eval[1] == "integer":
            return left_eval[0] + right_eval[0], "integer"
        elif left_eval[1] == right_eval[1] == "string":
            return left_eval[0] + right_eval[0], "string"
        else:
            raise Exception("unable to cast")

    # Working with all types
    elif main_operator[0] in ["==", "!="]:
        if main_operator[0] == '==':
            if left_eval[0] == right_eval[0]:
                return "true", "boolean"
            else:
                return "false", "boolean"
        elif main_operator[0] == '!=':
            if left_eval[0] != right_eval[0]:
                return "true", "boolean"
            else:
                return "false", "boolean"


def _first_eval(expression: list, variable_dic):
    """Evaluates an expression (boolean, integer or string), where the input is a parsed list of tokens."""
    size = len(expression)
    if size == 0:
        raise Exception('Expression is empty.')
    elif size == 1:
        return _check_variable(expression[0], variable_dic)
    else:
        return _eval_global(expression, variable_dic)


def ext_eval_global(expression_str: str, variable_dic=None):
    """Evaluates an expression (boolean, integer or string), where the input is a string."""
    evaluated = _first_eval(parse(expression_str), variable_dic)
    if evaluated is None:
        return ""
    else:
        return evaluated[0]


def find_operator(expression):
    """Find the operator where to split an integer expression in two operands. We check from the end of the expression
    to the beggining (left associativity, from the lowest priority operator to the highest, ignoring operators in
    factors (between parenthesis)."""
    parenthesis = 0
    for j in range(7, -2, -1):
        for i in range(len(expression) - 1, -1, -1):
            # We have a "depth" of subexpressions, 0 being the root expression (increasing counter)
            if expression[i][1] == "parenthesis":
                if expression[i][0] == '(':
                    parenthesis += 1
                else:
                    parenthesis -= 1
            elif expression[i][1] == "operator":
                # If the operator has the priority we're looking for and we are not in a subexpression
                if expression[i][2] == j and parenthesis == 0:
                    return i


# FOR DEBUGGING PURPOSE ONLY
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

    # dict_var = {}
    # print(ext_eval_global("a = 10", dict_var))
    # print(ext_eval_global("a + 1", dict_var))
    # print(ext_eval_global("true and false and not true or false", dict_var))
    # print(ext_eval_global("-1"))
    # print(ext_eval_global("2-1"))
    print(ext_eval_global("1+*"))
    print(ext_eval_global("45 + 'Test'"))
    # print(ext_eval_global("-1 + -1 + (-1 - -1)"))
    # print(ext_eval_global("-1 + -1"))
    # print(ext_eval_global("(-2 - -4)"))
    # print(ext_eval_global("(0 + -1)"))
    # print(ext_eval_global("(-1)"))
    # print(ext_eval_global("(-1 - -1)"))
    # print(ext_eval_global("-(2 + 2)"))
    # print(ext_eval_global("-1 + -1 - (-1 - -1)"))
    # print(ext_eval_global("-1 + -1"))
    # print(ext_eval_global("(-1 + -1 - (-1 - -1))"))
    # print(ext_eval_global("((-1 + -1 - (-1 - -1)))"))
