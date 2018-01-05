# -*- coding: utf-8 -*-
from eval_global import ext_eval_global
import traceback
import logger_conf

logger = logger_conf.Log.logger

import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


clear()
print("Welcome to Expression Evaluator: Integer Only Edition.\nUse \"exit\" to exit console.")

while True:
    exp = input("? ")
    try:
        print(ext_eval_global(exp))
    except Exception as e:
        print(e)
        logger.error(str(e))
        logger.error(str(traceback.format_exc()))

clear()
