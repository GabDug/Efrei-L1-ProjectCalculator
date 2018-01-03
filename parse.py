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
            raise Exception(f"Error: loop limit reached while parsing. Can't parse {expression[i]} at {i}.")
        # logger.debug("=> ", tokens)
        if expression[i] in [" ", "\n", "\r"]:
            i += 1
            continue
        if expression[i] in "+-":
            tokens.append((expression[i], "operator", 2))
            i += 1
            continue
        if expression[i] in "/*":
            tokens.append((expression[i], "operator", 1))
            i += 1
            continue
        if expression[i] in "()":
            logger.debug("Parenthesis stack:" + str(parenthesis_stack))
            if expression[i] == "(":
                parenthesis_stack.append(i)
                parenthesis_id = i
            elif expression[i] == ")":
                parenthesis_id = parenthesis_stack[-1]
                del parenthesis_stack[-1]
            tokens.append((expression[i], "parenthesis", parenthesis_id))
            i += 1
            continue
        if expression[i] in "0123456789":
            j = i + 1
            while j < len(expression) and expression[j] in "0123456789":
                j += 1
            tup = (int(expression[i:j]), "integer")

            # Here we check for negative numbers
            # TODO Stop working with tuple, better code
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
            continue
        if expression[i] in string.ascii_letters:
            j = i + 1
            while j < len(expression) and expression[j] in string.ascii_letters + string.digits:
                j += 1
            if expression[i:j] == "true":
                tup = (expression[i:j], "boolean")
            elif expression[i:j] == "false":
                tup = (expression[i:j], "boolean")
            elif expression[i:j] == "not":
                tup = (expression[i:j], "operator", 4)
            elif expression[i:j] == "and":
                tup = (expression[i:j], "operator", 5)
            elif expression[i:j] == "or":
                tup = (expression[i:j], "operator", 6)

            else:
                tup = (expression[i:j], "variable")

            tokens.append(tup)
            i = j
            continue
        if expression[i] in "<>=!":
            j = i + 1
            while j < len(expression) and expression[j] == "=":
                j += 1
            if expression[i:j] == "=":
                tup = (expression[i:j], "assignment")
            elif expression[i:j] in ["==", "!=", "<=", ">=", "<", ">"]:
                tup = (expression[i:j], "operator", 3)
            else:
                tup = (expression[i:j], "unknown")
            tokens.append(tup)
            i = j
            continue
        if expression[i] in "'\"":
            j = i + 1
            while j < len(expression) and expression[j] != expression[i]:
                j += 1
            # TODO Check the condition for error, may be invalid
            if j == len(expression) or expression[j] != expression[i]:
                logger.error("Error: no ending symbol for string starting at " + str(i) + ".")
                raise Exception("Error: no ending symbol for string starting at " + str(i) + ".")
            # i+1 to j : string without the starting and ending symbol
            tokens.append((expression[i + 1:j], "string"))
            # restart after the ending symbol (' or "...)
            i = j + 1
            continue
    return tokens


def parse(expression: str) -> list:
    """Parse a string expression to a list of tuples."""

    list_expression = _expression_to_list(expression)
    logger.debug("List expression: " + str(list_expression))
    return list_expression


def remove_parenthesis(expression):
    """Remove useless global parenthesis. Works recursively."""
    # If there is a parenthesis at beginning and at the end, and they are matching.
    if expression[0][0] == '(' and expression[-1][0] == ')' and expression[0][2] == expression[-1][2]:
        return remove_parenthesis(expression[1:-1])
    else:
        return expression


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

    # logger.info(parse("'Salut'"))
    # logger.info(parse("'Salut'+'toi'"))
    # logger.info(parse("'Salut+'toi'"))
    logger.info(parse("3+4*2"))
    logger.info(parse("248+345"))
    logger.info(parse("(3 + 2) * 4"))
    logger.info(parse("3 - 4"))
    logger.info(parse("-4 + 3"))
    logger.info(parse("(-1) + -1 + (-1 - -1)"))
    logger.info(parse("(3+254)* 44 "))
    logger.info(parse("'Yo'"))
    logger.info(parse("'Hey''You'"))
    logger.info(parse("'Test' + 'os'"))
    # logger.info(parse("'test"))
    logger.info(parse("((1))"))
    logger.info(parse("(1)*(2)"))
    logger.info(parse("(1+(2*3))"))
    logger.info(parse("(1+(2*3))(4*5)"))
    logger.info(parse("((1+(2*3))(4*5))"))
    logger.info(parse("(4+6)-5*9"))
    logger.info(parse("true"))
    logger.info(parse("true and false"))
    logger.info(parse("1 < 5 and 5 < 10"))
    logger.info(parse("1+ 2 +3 == 2 * 3"))
    logger.info(parse("test = 2 * 3"))
