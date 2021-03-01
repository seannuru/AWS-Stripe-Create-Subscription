import boto3
import stripe
import json
import os
from config import Config


class StripeApiManager(Config):
    _stripe = None
    customer = {}
    def __init__(self, event):
        super().__init__()
        self._stripe = stripe
        self._stripe.api_key = self.conf('STRIPE_SECRET_KEY')

        self.request = event['request']
        self.user_attributes = self.request['userAttributes']
        self.user = {
            'username': event['userName'],
            'email': self.user_attributes.get('email'),
            'sub': self.user_attributes.get('sub'),
            'App client ID': event['callerContext'].get('clientId'),
            'Trigger function': event['triggerSource'],
            'User pool': event['userPoolId']
        }

    def create_stripe_customer(self):
        description = '\n'.join([k + ': ' + str(v) for k, v in self.user.items()])
        self.customer = self._stripe.Customer.create(
            email=self.user['email'],
            name=self.user['username'],
            description=description
        )
        return self.customer

    def create_subscription(self):
        self.subscription = {}
        if 'id' in self.customer:
            self.subscription = self._stripe.Subscription.create(
              customer=self.customer['id'],
              items=[
                {"price": self.conf('STRIPE_PRICE_PLAN')},
              ],
            )
        return self.subscription

    def create_payment_method(self):
        # create sample payment method
        self.payment = self._stripe.PaymentMethod.create(
          type="card",
          card={
            "number": "4242424242424242",
            "exp_month": 2,
            "exp_year": 2022,
            "cvc": "314",
          },
        )

    def attach_payment_method_to_customer(self):
        self.customer_payment_method = {}
        if self.payment['id'] and self.customer['id']:
            self.customer_payment_method = self._stripe.PaymentMethod.attach(
              self.payment['id'],
              customer=self.customer['id']
            )
        return self.customer_payment_method

    def update_customer_invoice_payment_method(self):
        self.customer = self._stripe.Customer.modify(
          self.customer['id'],
          invoice_settings={
              "default_payment_method": self.customer_payment_method['id']
          },
        )
