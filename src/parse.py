import logging
import string
from sys import stdout

if __name__ != "__main__":
    import logging

    logger = logging.getLogger(__name__)


def _expression_to_list(expression: str) -> list:
    """Output a list of tokens (tuples) from a string."""
    tokens = []
    parenthesis_stack = []

    i = 0
    loop_count = 0
    length = len(expression)
    while i < length:
        loop_count += 1
        if loop_count > 10000:
            raise Exception(f"loop limit reached while parsing. Can't parse {expression[i]} at {i}.")
        # logger.debug("=> ", tokens)
        if expression[i] in [" ", "\n", "\r"]:
            i += 1
        elif expression[i] in "+-":
            tokens.append((expression[i], "operator", 2))
            i += 1
        elif expression[i] in "/*":
            tokens.append((expression[i], "operator", 1))
            i += 1
        elif expression[i] in "()":
            logger.debug("Parenthesis stack:" + str(parenthesis_stack))
            if expression[i] == "(":
                parenthesis_stack.append(i)
                parenthesis_id = i
            elif expression[i] == ")":
                # If we have a closing parenthesis and no open parenthesis, raise Exception
                if parenthesis_stack == []:
                    raise Exception("unmatched parenthesis (')')")
                parenthesis_id = parenthesis_stack[-1]
                del parenthesis_stack[-1]
            tokens.append((expression[i], "parenthesis", parenthesis_id))
            i += 1
        elif expression[i] in "0123456789":
            j = i + 1
            while j < len(expression) and expression[j] in "0123456789":
                j += 1
            tup = (int(expression[i:j]), "integer")

            # Here we check for negative numbers
            if i != 0 and tokens[-1][0] == "-":
                if (i == 1 or tokens[-2][1] != "integer") and not (i > 2 and tokens[-2][0] == ")"):
                    # remove the operator
                    del tokens[-1]
                    tup = (-1 * tup[0], tup[1])
                    tokens.append(tup)
                else:
                    tokens.append(tup)
            else:
                tokens.append(tup)
            i = j
        elif expression[i] in string.ascii_letters:
            j = i + 1
            while j < len(expression) and expression[j] in string.ascii_letters + string.digits:
                j += 1
            if expression[i:j] == "true":
                tup = ("true", "boolean")
            elif expression[i:j] == "false":
                tup = ("false", "boolean")
            elif expression[i:j] == "not":
                tup = ("not", "operator", 4)
            elif expression[i:j] == "and":
                tup = ("and", "operator", 5)
            elif expression[i:j] == "or":
                tup = ("or", "operator", 6)
            else:
                tup = (expression[i:j], "variable")

            tokens.append(tup)
            i = j
        elif expression[i] in "<>=!":
            j = i + 1
            while j < len(expression) and expression[j] == "=":
                j += 1
            if expression[i:j] == "=":
                tup = (expression[i:j], "operator", 7)
            elif expression[i:j] in ["==", "!=", "<=", ">=", "<", ">"]:
                tup = (expression[i:j], "operator", 3)
            else:
                tup = (expression[i:j], "unknown")
            tokens.append(tup)
            i = j
        elif expression[i] in "'\"":
            j = i + 1
            while j < len(expression) and expression[j] != expression[i]:
                j += 1
            if j == len(expression) or expression[j] != expression[i]:
                logger.error("Error: no ending symbol for string starting at " + str(i) + ".")
                raise Exception("no ending symbol for string starting at " + str(i) + ".")
            # i+1 to j : string without the starting and ending symbol
            tokens.append((expression[i + 1:j], "string"))
            # restart after the ending symbol (' or "...)
            i = j + 1
        else:
            raise Exception(f"unknown character {expression[i]} at {i}.")
    if parenthesis_stack != []:
        raise Exception("unmatched parenthesis ('(')")
    return tokens


def parse(expression: str) -> list:
    """Parse a string expression to a list of tuples."""

    list_expression = _expression_to_list(expression)
    logger.debug("List expression: " + str(list_expression))
    return list_expression


def remove_parenthesis(expression):
    """Remove useless global parenthesis. Works recursively."""
    # If there is a parenthesis at beginning and at the end, and they are matching.
    try:
        if expression != [] and expression[0][0] == '(' and expression[-1][0] == ')' and expression[0][2] == \
                expression[-1][2]:
            return remove_parenthesis(expression[1:-1])
        else:
            return expression
    except IndexError as e:
        logger.error("Error: index error: " + str(e))
        raise Exception("missing operand near " + str(expression))


# FOR DEBUGGING PURPOSE ONLY
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
    formatter.datefmt = "%H:%M:%S"
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.info("Starting logger from module.")

    logger.info(parse("1 + 3 * 4 - 5"))
    logger.info(parse("(1 + 3 * 5 - 6) + (4 / 7)"))
