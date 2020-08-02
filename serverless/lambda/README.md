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
