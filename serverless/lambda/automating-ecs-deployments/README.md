# Automating ECS Deployments

![image](https://user-images.githubusercontent.com/35857179/83323905-4550bc80-a294-11ea-8a87-0d75e44ad6b4.png)

## Prerequisite

- S3 bucket for storing logs
- Lambda Executation Role ``lambda_exec_role``
- Existing ECS Cluster
- Existing ECR Repository

## Create Our Lambda Function
With everything ready to go, it's time to set up our Lambda function. To start, download the provided Lambda function using the supplied wget command.

wget https://raw.githubusercontent.com/linuxacademy/content-lambda-deep-dive/master/section_6/live_activity_12/lambda_function.py
Next, using the zipwe downloaded, we want to zip up the function so we can upload it to Lambda using zip lambda_function.zip.

Now, run the aws lambda create-function command that is supplied:

```
aws lambda create-function \
--function-name ECS \
--handler lambda_function.lambda_handler \
--memory-size 1024 \
--timeout 15 \
--runtime python3.6 \
--zip-file fileb:///home/user/lambda_function.zip \
--role arn:aws:iam::123456789123:role/lambda_exec_role \
--environment Variables="{NAME=secondcontainer,IMAGE=URI,TASK_DEF=demotaskdef,CLUSTER=democluster,SERVICE=demoservice}"
```
Head back to the console. Go to theServices dropdown and select Lambda. Verify that the ECS function exists within the Lambda console.

In another tab, go to ECS and select Repositories. Select our repository, and then copy the Repository URI. Back on our previous page, under Environment variables replace the URI with what we just copied. Make sure to add :latest to the end of it. Select Save. Back on ECS, select Clusters and locate the Public IP. Enter it into a new browser tab. We are greeted with "Hello World!", meaning our Lambda function is ready.

## Create Our CloudTrail Trail and CloudWatch Event

With everything in place, we now need to configure our trail and trigger. To do so, we need to navigate to CloudTrail. Here, select Create Trail and make sure that All is selected for the Read/Write events. Under Storage Location, select No, and then choose the bucket provided. Select Create. We will see the new trail.

Now, click Linux located under Name on the table. Here, head down to CloudWatch Logs and select Configure. Leave it as the default and then select Continue and then Allow.

Navigate to the CloudWatch page, either by locating it on the Services page or searching for it in the search bar. Here we will see our default log group.

## Create a CloudWatch Rule

While we're here in CloudWatch, let's create our rule. To do so, select Rules from the sidebar, then Create rule. Select Event Pattern, then for the Service Name choose the EC2 Container Registry and AWS API Call via CloudTrail as the event type.

Next, for Specific operation, add PutImage as the operation name. In the Targets section, set it to Lambda Function and then select ECS for the Function. Finally, select Configure details. Provide it with a name and makes sure Enabled is selected. Now we need to make sure that the status is enabled. To do so, click on the rule. The page that appears shows our status.

## Test It Out

With our trail, event, and rules in place, it is time to test out everything we've done. To do so, go back to our Amazon ECS, and select Repositories. Select the one that we created.

With it opened, head back to our command line. Use cd docker/ to go back to our Docker directory. Now, enter vim static-html-directory/index.html. We don't have to use vim; it is just what we are using for this example.

In the document, add another header of "It Worked!" under "Hello World!", and then save the file.

With that updated, we need to rebuild our docker image. First run ``docker build -t hello .`` followed by docker tag hello:latest. Tag the image with latest and then, using the push command from before, push it to the repo in ECR.

Navigate back to CloudWatch or Lambda and wait for your invocation that lets you know it has updated. Once invoked, verify that our cluster has been updated in ECS. To do this, go back to Amazon ECS and select Cluster. Here, select the democluster, then demoservice. Lastly, select the Tasks tab and select the task.

On the task's page, look for the Public IP. Copy the IP and past it into your web browser. If we've done everything right, we will get a page that says, "Hello World! It worked!".