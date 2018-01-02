from eval_int import eval_int
from eval_str import eval_str
from parse import parse, remove_parenthesis
import logging

logger = logging.getLogger(__name__)

def single_element(element):
    """Evaluate a single token. Used when there is only one token."""
    if element[1] == "variable":
        if element[0] == "exit":
            logger.info("Exiting...")
            exit()
    elif element[1] == "integer":
        return element[0]
    elif element[1] == "string":
        return element[0]


def eval_global(expression: list):
    """Evaluates an expression (boolean, integer or string), where the input is a parsed list of tokens."""
    size = len(expression)
    if size == 0:
        return None
    elif size == 1:
        return single_element(expression[0])
    else:
        return eval_int(expression)


def ext_eval_global(expression_str: str):
    """Evaluates an expression (boolean, integer or string), where the input is a string."""
    return eval_global(parse(expression_str))


if __name__ == "__main__":
    logger.info(eval_global(parse("1")))
    logger.info(eval_global(parse("exit")))
