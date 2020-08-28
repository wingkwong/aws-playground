# Process Transaction Files

![image](https://user-images.githubusercontent.com/35857179/90503617-4f42d700-e182-11ea-8d2a-4ce5a2696dac.png)

## The Scenario workflow

- You will upload a transactions file to an Amazon S3 bucket

- This will trigger an AWS Lambda function that will read the file and insert records into two Amazon DynamoDB tables

- This will trigger another AWS Lambda function that will calculate customer totals and will send a message to an Amazon Simple Notification Service (SNS) Topic if the account balance is over $1500

- Amazon SNS will then send an email notification to you and will store a message in Amazon Simple Queue Service (SQS) queues to notify the customer and your credit collection department.

## Steps

- Create a Lambda Function to Process a Transactions File

- Create a Lambda Function to Calculate Transaction Totals and Notify About High Account Balances

- Create a Simple Notification Service (SNS) Topic

- Create Two Simple Queue Service Queues

- Testing the Serverless Architecture by Uploading a Transactions File

- Check the DynamoDB tables

- Check your SQS Queues

- Check your Lambda Functions
