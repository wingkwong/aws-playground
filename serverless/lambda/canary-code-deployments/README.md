# Canary Code Deployments

![image](https://user-images.githubusercontent.com/35857179/83275119-50a6d800-a201-11ea-936a-4eefbfaea5d6.png)

Create Your Lambda Function

Navigate to Lambda.

Click Create a function.

Make sure the Author from scratch option at the top is selected, and then use the following settings:

```
Name: Function
Runtime: Python 3.6
Role: Choose an existing role
Existing role: lambda_exec_role
```

Click Create function.

On the Function page, scroll to the Function code section.

```py
import json


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            'message': 'Hello World'
        })
    }
```

Click Save.

Publish Our First Version and Create Our First Alias

At the top, click Actions and select Publish new version.

Give it a description (e.g., "Version 1"), and click Publish.

In the Actions dropdown, select Create alias, and set the following values:

```
Name: PROD
Description: Prod
Version: 1
```

Click Create.

Create and Deploy Our API Within API Gateway

Navigate to API Gateway in a new browser tab.

Click Get Started.

Choose New API, and set the following values:

```
API name: Hello
Description: Hello
Endpoint Type: Regional
```

Click Create API.

On the Resources page, click Actions and select Create Resource from the dropdown.

Give it a Resource Name of "hello".

Click Create Resource.

Make sure you have the /hello resource selected, click Actions, and select Create Method.

In the Options dropdown, select GET and then click the checkmark.

In the /hello - GET - Setup window, set the following values:


```
Integration type: Lambda Function
Use Lambda Proxy integration: Check
Lambda Region: us-east-1
Lambda Function: Function:PROD
Use Default Timeout: Check
```

Click Save.

Click Actions and select Deploy API.

In the Deploy API dialog, set the following values:

```
Deployment stage: [New Stage]
Stage name: One
Stage description: One
Deployment description: One
```

Click Deploy.

In the One - GET - /hello section, open the invoke URL in a new browser tab. We should see the message we added in our Lambda code.

Publish Version 2 of Our Function and Update Our Alias

In the Lambda console, click the Alias:PROD dropdown and select $LATEST.

```py
import json
import os


def lambda_handler(event, context):
    ip = event['requestContext']['identity']['sourceIp']

    return {
        "statusCode": 200,
        "body": json.dumps({
            'message': 'Hello World!',
            'location': ip
        })
    }
```

Click Save.

Click Actions and select Publish new version.

Give it a description (e.g., "Version 2"), and click Publish.


In the Version: 2 dropdown, select the Aliases tab and click the PROD alias.

Scroll to the Aliases section, and set the Additional Version to 2.

Set the weight to 50%.

Click Save.

Refresh the browser tab with the invoke URL a few times to verify you are getting different versions of code based on the response.