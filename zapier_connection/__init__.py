import logging
import sys

LOGGING_FOMRAT = '[%(asctime)s: %(module)s -> %(filename)s] --> %(message)s'

logging.basicConfig(
    format=LOGGING_FOMRAT,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
