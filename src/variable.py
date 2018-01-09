
def variable_init(expression, variable_list):
    """initialize variable if needed"""
    if len(expression) == 3:
        if expression[0][1] == "variable" and expression[1][0] == "=":
            if expression[2][1] != "variable":
                variable_list[expression[0][0]] = expression[2][0]
            elif expression[2][1] == "variable" and expression[2][1] in variable_list:
                variable_list[expression[0][0]] = expression[2][0]


def convert_var(expression, variable_list):


def variable_analyzing(expression, variable_list):
    """Analyse the expression and give value to variable"""

    for i in range(len(expression)):
        if expression[i][1] == "variable":
            if expression[i][0] in variable_list:
                expression[i][0] = variable_list[expression[i][0]]
                expression[i][1] = "integer"
            elif expression[i][0] not in variable_list and expression[i + 1]
