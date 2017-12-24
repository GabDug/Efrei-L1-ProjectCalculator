from eval_global import *
from parse import parse

print("Expression Evaluator: Integer Only Edition")
while True:
    exp = input("? ")
    print(eval_global(parse(exp)))
