# Simple Function

![image](https://user-images.githubusercontent.com/35857179/83324319-138d2500-a297-11ea-9f13-01ed49afd084.png)

Create a Lambda Function within the AWS Lambda Console

Navigate to Lambda.

Click Create a function.

Make sure the Author from scratch option at the top is selected, and then use the following settings:

```
Basic information:
Name: HelloWorld
Runtime: Python3.6
Permissions:
Select Choose or create an execution role.
Execution role: Use an existing role
Existing role: lambdarole
```
Click Create function.

On the HelloWorld page, scroll to the Function code section.

Delete the existing code there, and enter the below code.

```py
import json

print('Loading your function')

def lambda_handler(event, context):
    # print statements actually get printed to the logs.
    print("message --> " + event['message'])

    # Actually returning the value of the 'message' key.
    return event['message']

    # Raising an exception if something goes wrong...
    raise Exception('Something went wrong!')
```

Click Save.

Create a Test Event and Manually Invoke the Function Using the Test Event

In the dropdown next to Test at the top of the Lambda console, select Configure test events.

In the dialog, select Create new test event.

Select the Hello World event template.

Give it an event name (e.g., "Test").

Replace the current code there with the provided JSON code, and then click Create.

Click Test to verify the function's success.

Verify That CloudWatch Has Captured Function Logs

Navigate to CloudWatch.

Select Logs in the left-hand menu.

Select the log group with your function name in it.

Select the log stream within the log group.

Verify the output is present and correct.

![image](https://user-images.githubusercontent.com/35857179/83324299-e2145980-a296-11ea-8fb3-eeb2021f876c.png)

