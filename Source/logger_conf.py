class Log:
    from sys import stdout

    import logging

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Terminal log
    ch = logging.StreamHandler(stdout)
    ch.setLevel(logging.DEBUG)

    # File log
    f = logging.FileHandler("calculator.log", mode="w")
    f.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(filename)s] : %(message)s")
    formatter.datefmt = "%H:%M:%S"

    ch.setFormatter(formatter)
    f.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(f)

    logger.info("Starting logger")

