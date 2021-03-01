import os
import boto3
import json
import sys

class Config(object):
    _conf = {}
    def __init__(self):
        Config._conf = {}
        # secrets manager
        client = boto3.client('secretsmanager')
        keys = json.loads(
            client.get_secret_value(SecretId = os.environ['SECRET_MANAGER'])['SecretString'])
        # get stripe keys
        Config._conf['STRIPE_PUBLIC_KEY'] = keys['stripe-public']
        Config._conf['STRIPE_SECRET_KEY'] = keys['stripe-secret']
        # get Product price or plan
        Config._conf['STRIPE_PRICE_PLAN'] = os.environ['STRIPE_PRICE_PLAN']

    @staticmethod
    def conf(name):
        return Config._conf[name]

    @staticmethod
    def set_conf(name, value):
        Config._conf[name] = value
