import json
import os
import sys
from stripe_api import StripeApiManager

def lambda_handler(event, context):
    # get user attributes from cognito
    request = event.get('request')
    if 'userAttributes' in request:
        stripe_obj = StripeApiManager(event)
        print(stripe_obj.create_stripe_customer())
        print(stripe_obj.create_payment_method())
        print(stripe_obj.attach_payment_method_to_customer())
        print(stripe_obj.update_customer_invoice_payment_method())
        print(stripe_obj.create_subscription())
    print(event)
    # Return to Amazon Cognito
    return event
