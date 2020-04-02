import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'one-hundred-percents-random-key-you-never-hack'