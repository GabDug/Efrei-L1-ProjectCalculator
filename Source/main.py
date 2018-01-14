# -*- coding: utf-8 -*-
import traceback
from os import system, name

import logger_conf
from eval_global import ext_eval_global

logger = logger_conf.Log.logger


def clear():
    system('cls' if name == 'nt' else 'clear')


variable_list = {}

clear()

print("Welcome to the Calculator.\nUse \"exit\" to exit console or hit enter twice.")

exit = False

while True:
    logger.debug("Variable dic: " + str(variable_list))
    exp = input("? ")

    # If the user just pressed enter
    if exp == "":
        # If it's the second time in a row, exit
        if exit:
            break
        else:
            exit = True
            print("Press enter again to quit.")
            continue
    # If he has entered a not-empty expression, reset
    else:
        if exit:
            exit = False

    # Try to evaluate and print....
    try:
        res = ext_eval_global(exp, variable_list)
        if res != "":
            print(res)
    # Catch the exception eval can raise
    except Exception as e:
        print("Error: " + str(e))
        logger.error(str(e))
        logger.error(str(traceback.format_exc()))

clear()
