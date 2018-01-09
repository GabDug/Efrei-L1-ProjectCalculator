
def find_type(token):
    pass

def variable_init(expression, variable_list):
    """initialize variable if needed"""
    if len(expression) == 3:
        if expression[0][1] == "variable" and expression[1][1] == "assignment":
            if expression[2][1] != "variable":
                variable_list[expression[0][0]] = expression[2][0]
                expression.remove(expression[2])
                expression.remove(expression[1])
            elif expression[2][1] == "variable" and expression[2][1] in variable_list:
                variable_list[expression[0][0]] = expression[2][0]


def convert_var(expression, variable_list):
    for element in expression:
        if element[1] == "variable":
            if element[0] in variable_list:
                element = (variable_list[element[0]], find_type(variable_list[element[0]]))


def variable_analyzing(expression, variable_list):
    """Analyse the expression and give value to variable"""

    variable_init(expression, variable_list)
