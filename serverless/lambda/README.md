# Lambda

**If your code is not executing, you aren’t being charged!**

## Optimize Costs

- Colocating aws regions
    - moving your functions to the same region to reduce data transfer between those services
- Refractoring and rewriting 
- Caching

## Limits

API Gateway quotas for configuring and running a REST API

```
50 milliseconds - 29 seconds for all integration types, including Lambda, Lambda proxy, HTTP, HTTP proxy, and AWS integrations.
```

Lambda Function timeout

```
900 seconds (15 minutes)
```

### Timeout Problem

If the API is callign a third-part service to retrieve the data and it is not responding. The function has a timeout of 15 mintues but you will receive the timeout error after 29 seconds. 

### Solution

Set your own timeouts at the function level - let's say 3-6 seconds - so that we don't need to wait for an unreasonable time for a downstream response. If it is for Kinesis, DynamoDB Streams or SQS, adjust it based on the batch size instead.

However, giving a fixed timeout limit at the function and integration level doesn't make full use of the execution time and cause problems. To utilize the invocation time better, set the timeout based on the amount of invocation time left accounting for the recovery steps.

```js
var server = app.listen();
server.setTimeout(6000);
And to set the timeout for each API call, we can use this code:

app.post('/xxx', function (req, res) {
  req.setTimeout( context.getRemainingTimeInMills() - 500 ); // 500ms to account recovery steps
});
```

If the average execution time for your function is 110ms , increase the memory to bring it below 100ms to avoid from being charged for 200ms as AWS charges for lambda usage down to a fraction of 100ms. 

If your function is taking more time than the timeout value, consider to break it into smaller pieces using Step Functions.

## Concurrency

AWS Lambda provides two features for controlling concurrency: Reserved Concurrency and Provisioned Concurrency Scaling. These features allow you to manage the number of concurrent executions of your Lambda functions, ensuring that your application can handle the desired level of traffic.

### Reserved Concurrency:

Reserved Concurrency allows you to set a fixed limit on the maximum number of concurrent executions for a specific Lambda function. This setting ensures that the function never exceeds the defined concurrency limit, regardless of the number of incoming requests. Reserved Concurrency provides a static concurrency control mechanism, and it's useful when you want to allocate a dedicated capacity for critical functions or prevent unexpected spikes in concurrent executions.

### Provisioned Concurrency:

Provisioned Concurrency enables you to pre-warm your Lambda functions by specifying the desired number of concurrent executions to be provisioned. Instead of relying on the on-demand scaling behavior, Provisioned Concurrency keeps a set number of instances ready to respond to incoming requests instantly. This feature is particularly useful for latency-sensitive applications or when you need to reduce the "cold start" latency experienced by functions that are invoked infrequently.

The main differences between Reserved Concurrency and Provisioned Concurrency Scaling are:

- Control: Reserved Concurrency provides a fixed limit on the maximum number of concurrent executions, while Provisioned Concurrency Scaling allows you to specify the desired number of concurrent executions to be provisioned.
- Scaling behavior: Reserved Concurrency does not scale dynamically and remains constant regardless of the incoming request rate. Provisioned Concurrency Scaling dynamically adjusts the number of provisioned instances based on the incoming request rate, ensuring that the desired concurrency level is maintained.
- Cost: Reserved Concurrency is billed based on the number of reserved concurrency units, while Provisioned Concurrency Scaling is billed based on the number of provisioned concurrency units and the duration they are active.
