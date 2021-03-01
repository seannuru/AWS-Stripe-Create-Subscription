## AWS Lambda function for creating Stripe User Subscription

### User fields comes from Cognito pools in event['request']

### Make sure you have these env variables on AWS lambda 
STRIPE_SECRET_KEY - ARN for your secret manager, in secret manager you should save your Sprite public and private keys
STRIPE_PRICE_PLAN - price plan on Stripe

### all methods print return values, you can see AWS Lmbda logs
