import os
from openai import OpenAI
from dotenv import load_dotenv
import logging
from logging.config import dictConfig
import sys
import datetime


def sql_Test(string1, string2):
    load_dotenv()
    client = OpenAI(
        api_key=(os.getenv('OPENAI_API_KEY2'))
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are part of a automated system to detect sql injections. "
            "We will send you a string, and you need to return 0 if it is NOT sql injection, return 1 if it is. "
            "Only return 1 or 0, nothing else."},
            {"role": "user", "content": "Are either of these sql injection? " + string1 + " " + string2}
        ]
    )

    if response.choices[0].message.content == '1':
        try:
            Logger(response, "Username Input: " + string1 + " " + "Password Input : " + string2)
        except OSError:
            return 1
        return 1
    else:
        return 0

def testEnvPath():
    load_dotenv()
    print(os.getenv('OPENAI_API_KEY2'))

def gen_LogName(prefix, extension):
    current_date=datetime.datetime.now().strftime('%Y-%m-%d %H%M%S')
    return f"WASPGpt/logs/{prefix}_{current_date}_{extension}"

def Logger(content, content2):
    logging_config = dict(
        version=1,
        formatters={
            'verbose': {
                'format': ("[%(asctime)s] %(levelname)s "
                           "[%(name)s:%(lineno)s] %(message)s"),
                'datefmt': "%d/%b/%Y %H:%M:%S",
            },
            'simple': {
                'format': '%(levelname)s %(message)s',
            },
        },
        handlers={
            'api-logger': {'class': 'logging.handlers.RotatingFileHandler',
                           'formatter': 'verbose',
                           'level': logging.DEBUG,
                           'filename': gen_LogName(prefix='wasp', extension='log'),
                           'maxBytes': 52428800,
                           'backupCount': 7},
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple',
                'stream': sys.stdout,
            },
        },
        loggers={
            'api_logger': {
                'handlers': ['api-logger', 'console'],
                'level': logging.DEBUG
            }
        }
    )

    dictConfig(logging_config)
    api_logger = logging.getLogger('api_logger')
    api_logger.info(content)
    api_logger.info(content2)
