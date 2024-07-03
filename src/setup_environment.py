import logging
import os
import boto3
import botocore.exceptions
import json
import base64


def get_logger(*args):
    if args:
        start = args[0]
        log_file = args[1]

        if os.path.isabs(log_file):
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
            datefmt='%Y-%m-%d %H:%m:%S',
        )
        logger = logging.getLogger()
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)
        logger.info('Starting logger %s', start)
        return logger

