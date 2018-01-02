from eval_global import ext_eval_global
import traceback
import logger_conf

logger = logger_conf.Log.logger


print("Expression Evaluator: Integer Only Edition")

while True:
    exp = input("? ")
    try:
        print(ext_eval_global(exp))
    except Exception as e:
        print(e)
        print(traceback.format_exc())
