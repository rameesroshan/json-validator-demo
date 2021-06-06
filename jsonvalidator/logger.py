import logging


def get_logger(name: str) -> object:
    """
    Wrapper for standard logging.
    """
    log_file = f"/jsonvalidator/logs/validator.log"
    format = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file, mode='a')
    handler = logging.StreamHandler()
    formatter = logging.Formatter(format)
    handler.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(fh)

    return logger