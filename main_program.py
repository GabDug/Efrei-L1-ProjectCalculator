from eval_int import eval_int
from parse import parse


print("Expression Evaluator: Integer Only Edition")
while True:
    exp = input("? ")
    print(eval_int(parse(exp)))
